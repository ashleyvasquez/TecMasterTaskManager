
# Documentación del Proyecto 2

## 1. Lenguaje de programación
El lenguaje de programación utilizado en este proyecto es Python. Python es un lenguaje de alto nivel, interpretado y de propósito general, que es ampliamente utilizado en el desarrollo de aplicaciones web, análisis de datos, inteligencia artificial y más.

## 2. Frameworks/Toolkits

El proyecto utiliza los siguientes frameworks y herramientas:

- **Flask:** Un micro-framework para Python que permite desarrollar aplicaciones web de manera sencilla y rápida.
- **Flasgger:** Una extensión para Flask que facilita la creación de documentación de API utilizando OpenAPI (Swagger). Permite generar automáticamente la documentación interactiva de la API, lo que mejora la usabilidad y facilita el desarrollo.


## 3. Tecnología
El proyecto está construido utilizando tecnologías modernas que permiten una alta eficiencia y facilidad de uso, incluyendo:
- **Docker**: para la contenedorización de la aplicación, asegurando que funcione de manera consistente en diferentes entornos.
- **JSON**: como formato de intercambio de datos, que permite una fácil integración con otros sistemas y lenguajes de programación.
- **OpenAPI**: para documentar y definir la API de manera estructurada, facilitando la comprensión y el uso por parte de los desarrolladores.

## 4. Estándares de programación
Se siguen los siguientes estándares de programación en el desarrollo de este proyecto:
- **REST**: principios de arquitectura para el diseño de APIs que utilizan el protocolo HTTP, permitiendo la comunicación entre el cliente y el servidor de manera eficiente y estructurada.

## 5. Los argumentos que recibe y responde el API

La API implementada en este proyecto incluye las siguientes rutas y sus respectivas operaciones:

### 5.1. Obtener todas las tareas

- **Método:** `GET`
- **Ruta:** `/tasks`
- **Descripción:** Obtiene todas las tareas organizadas en las secciones "Por Hacer", "En Progreso" y "Hecho".
- **Parámetros:**
  - No se requieren parámetros.
- **Respuesta:**
  - **Código 200:** `application/json` con la estructura de datos de las tareas.
  - **Ejemplo de respuesta:**
    ```json
    {
      "En Progreso": [
        {
          "description": "Hacer un tablero Kanban",
          "id": 1,
          "status": "En Progreso",
          "title": "Proyecto2"
        }
      ],
      "Hecho": [
        {
          "description": "Hacer una máquina virtual",
          "id": 2,
          "status": "Hecho",
          "title": "Lab2"
        }
      ],
      "Por Hacer": []
    }
    ```

### 5.2. Agregar una tarea

- **Método:** `POST`
- **Ruta:** `/tasks`
- **Descripción:** Agrega una nueva tarea.
- **Parámetros:**
  - **Body:** Debe incluir un objeto JSON con la siguiente estructura:
    - `title` (string, requerido): Título de la tarea.
    - `description` (string, requerido): Descripción de la tarea.
- **Respuesta:**
  - **Código 201:** Tarea creada exitosamente.
  - **Código 400:** Solicitud mal formulada.
  - **Ejemplo de respuesta exitosa:**
    ```json
    {
      "message": "Tarea creada exitosamente",
      "task": {
        "id": 3,
        "title": "Nueva Tarea",
        "description": "Descripción de la nueva tarea",
        "status": "Por Hacer"
      }
    }
    ```

### 5.3. Mover una tarea

- **Método:** `PUT`
- **Ruta:** `/tasks/<id>/move`
- **Descripción:** Mueve una tarea de una sección a otra.
- **Parámetros:**
  - **URL:** `<id>` (integer, requerido): ID de la tarea a mover.
  - **Body:** Debe incluir un objeto JSON con la siguiente estructura:
    - `status` (string, requerido): Nuevo estado de la tarea ("Por Hacer", "En Progreso", "Hecho").
- **Respuesta:**
  - **Código 200:** Tarea movida exitosamente.
  - **Código 404:** Tarea no encontrada.
  - **Ejemplo de respuesta exitosa:**
    ```json
    {
      "message": "Tarea movida exitosamente",
      "task": {
        "id": 1,
        "title": "Proyecto2",
        "description": "Hacer un tablero Kanban",
        "status": "Hecho"
      }
    }
    ```

### 5.4. Eliminar una tarea

- **Método:** `DELETE`
- **Ruta:** `/tasks/<id>`
- **Descripción:** Elimina una tarea.
- **Parámetros:**
  - **URL:** `<id>` (integer, requerido): ID de la tarea a eliminar.
- **Respuesta:**
  - **Código 204:** Tarea eliminada exitosamente.
  - **Código 404:** Tarea no encontrada.
