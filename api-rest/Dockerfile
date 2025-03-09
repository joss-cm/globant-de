# Usa la imagen de Python
FROM python:3.10

# Configura el directorio de trabajo
WORKDIR /app

# Instala dependencias primero para aprovechar caché
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia los archivos al contenedor
COPY . /app

# Instala FastAPI y Uvicorn
RUN pip install fastapi uvicorn

# Expone el puerto 8000
EXPOSE 8000

# Comando por defecto para correr la API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]