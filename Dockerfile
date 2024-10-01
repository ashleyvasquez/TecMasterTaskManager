# Usa una imagen de Python compatible con ARM64
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt y luego instala las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto 5000 (o el que uses en tu app Flask)
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python3", "app.py"]
