from flask import Flask, jsonify, request, render_template
import json
from flasgger import Swagger

app = Flask(__name__)

# Inicializar Swagger
swagger = Swagger(app)

# Ruta del archivo JSON donde se almacenan las tareas
TASKS_FILE = 'tasks.json'

# Cargar tareas desde el archivo JSON
def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"Por Hacer": [], "En Progreso": [], "Hecho": []}

# Guardar tareas en el archivo JSON
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Ruta para la página principal con la interfaz del tablero Kanban
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Obtener todas las tareas
    ---
    responses:
      200:
        description: Una lista de tareas divididas en columnas
        content:
          application/json:
            schema:
              type: object
              properties:
                Por Hacer:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: El ID de la tarea
                      title:
                        type: string
                        description: El título de la tarea
                      description:
                        type: string
                        description: La descripción de la tarea
                      status:
                        type: string
                        description: El estado de la tarea
                En Progreso:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      title:
                        type: string
                      description:
                        type: string
                      status:
                        type: string
                Hecho:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      title:
                        type: string
                      description:
                        type: string
                      status:
                        type: string
    """
    tasks = load_tasks()
    return jsonify(tasks)

# Ruta para agregar una nueva tarea
@app.route('/tasks', methods=['POST'])
def add_task():
    """
    Agregar una nueva tarea
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
    responses:
      201:
        description: Tarea creada
    """
    tasks = load_tasks()
    data = request.get_json()

    new_task = {
        "id": len(tasks["Por Hacer"]) + len(tasks["En Progreso"]) + len(tasks["Hecho"]) + 1,
        "title": data["title"],
        "description": data.get("description", ""),
        "status": "Por Hacer"
    }

    tasks["Por Hacer"].append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

# Ruta para mover una tarea entre columnas
@app.route('/tasks/<int:task_id>/move', methods=['PUT'])
def move_task(task_id):
    """
    Mover una tarea entre columnas
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          type: object
          properties:
            status:
              type: string
              enum: ["Por Hacer", "En Progreso", "Hecho"]
    responses:
      200:
        description: Tarea movida
      404:
        description: Tarea no encontrada
    """
    tasks = load_tasks()
    data = request.get_json()
    new_status = data['status']

    for column in tasks:
        for task in tasks[column]:
            if task['id'] == task_id:
                tasks[column].remove(task)
                task['status'] = new_status
                tasks[new_status].append(task)
                save_tasks(tasks)
                return jsonify(task), 200

    return jsonify({"error": "Task not found"}), 404

# Ruta para eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Eliminar una tarea
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tarea eliminada correctamente
      404:
        description: Tarea no encontrada
    """
    tasks = load_tasks()

    for column in tasks:
        for task in tasks[column]:
            if task['id'] == task_id:
                tasks[column].remove(task)
                save_tasks(tasks)
                return jsonify({"message": "Task deleted successfully"}), 200

    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
