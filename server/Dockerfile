# Imagen base con Python
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements.txt y luego instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del backend
COPY . .

# Exponer el puerto de la API
EXPOSE 8000

# Comando para arrancar FastAPI con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
