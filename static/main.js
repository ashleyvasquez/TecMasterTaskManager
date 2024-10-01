// Función para obtener todas las tareas y mostrarlas en el tablero
async function loadTasks() {
    const response = await fetch('/tasks');
    const tasks = await response.json();

    for (const [status, taskList] of Object.entries(tasks)) {
        const column = document.getElementById(`tasks-${status.toLowerCase().replace(' ', '-')}`);
        column.innerHTML = '';
        taskList.forEach(task => addTaskToColumn(task, status));
    }
}

// Función para agregar una tarea al servidor y al tablero
document.getElementById('task-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;

    // Enviar la tarea al servidor (API)
    const response = await fetch('/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: title, description: description })
    });

    const newTask = await response.json();
    alert('Tarea añadida: ' + newTask.title);

    // Limpiar el formulario
    document.getElementById('task-form').reset();

    // Actualizar el tablero visualmente
    addTaskToColumn(newTask, "Por Hacer");
});

// Función para añadir tareas visualmente en las columnas del tablero
function addTaskToColumn(task, column) {
    const taskDiv = document.createElement('div');
    taskDiv.className = 'task';
    taskDiv.dataset.id = task.id;
    taskDiv.innerHTML = `
        <div class="task-title">${task.title}</div>
        <div>${task.description}</div>
        <button onclick="moveTask(${task.id}, 'Por Hacer')">Mover a Por Hacer</button>
        <button onclick="moveTask(${task.id}, 'En Progreso')">Mover a En Progreso</button>
        <button onclick="moveTask(${task.id}, 'Hecho')">Mover a Hecho</button>
        <button onclick="deleteTask(${task.id})">Eliminar</button>
    `;
    document.getElementById(`tasks-${column.toLowerCase().replace(' ', '-')}`).appendChild(taskDiv);
}

// Función para mover una tarea entre columnas
async function moveTask(taskId, newStatus) {
    const response = await fetch(`/tasks/${taskId}/move`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: newStatus })
    });

    if (response.ok) {
        alert('Tarea movida a ' + newStatus);
        loadTasks(); // Volver a cargar todas las tareas para actualizar el tablero
    } else {
        alert('Error al mover la tarea');
    }
}

// Función para eliminar una tarea
async function deleteTask(taskId) {
    const response = await fetch(`/tasks/${taskId}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        alert('Tarea eliminada');
        loadTasks(); // Volver a cargar todas las tareas para actualizar el tablero
    } else {
        alert('Error al eliminar la tarea');
    }
}

// Cargar las tareas cuando la página se carga
window.onload = loadTasks;
