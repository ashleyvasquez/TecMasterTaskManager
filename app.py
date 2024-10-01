from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__)

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
    tasks = load_tasks()
    return jsonify(tasks)

# Ruta para agregar una nueva tarea
@app.route('/tasks', methods=['POST'])
def add_task():
    tasks = load_tasks()
    data = request.get_json()

    new_task = {
        "id": len(tasks["Por Hacer"]) + len(tasks["En Progreso"]) + len(tasks["Hecho"]) + 1,
        "title": data["title"],
        "description": data.get("description", ""),
        "status": "Por Hacer"
    }

    # Añadir la nueva tarea a la columna "Por Hacer"
    tasks["Por Hacer"].append(new_task)
    
    # Guardar la tarea en el archivo JSON
    save_tasks(tasks)

    return jsonify(new_task), 201

# Ruta para mover una tarea entre columnas
@app.route('/tasks/<int:task_id>/move', methods=['PUT'])
def move_task(task_id):
    tasks = load_tasks()
    data = request.get_json()
    new_status = data['status']

    # Buscar y mover la tarea
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
    tasks = load_tasks()

    # Buscar y eliminar la tarea
    for column in tasks:
        for task in tasks[column]:
            if task['id'] == task_id:
                tasks[column].remove(task)
                save_tasks(tasks)
                return jsonify({"message": "Task deleted successfully"}), 200

    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  

