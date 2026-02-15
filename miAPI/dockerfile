#importamos la imagen base de python
FROM python:3.12-slim

#crear carpeta de trabajp
WORKDIR /app

#copiar requerimientos
COPY requirements.txt .

#instalar requerimietos dentro del contenedor no guardes cache 
RUN pip install --no-cache-dir -r requirements.txt

#Copiar archivo de la API
COPY ./app ./app

#exponer el puerto
EXPOSE 5000

#comando para ejecutar FASTAPI
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","5000","--reload"]