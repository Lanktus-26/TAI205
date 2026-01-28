#1. importaciones
from fastapi import FastAPI

#2. inicializacion APP
app= FastAPI()

#3. endpoints
@app.get("/")
async def holaMundo():
    return {"mensaje":"Hola Mundo FASTAPI"}

@app.get("/Bienvenidos")
async def Bienvenidos():
    return {"mensaje":"Bienvenidos"}