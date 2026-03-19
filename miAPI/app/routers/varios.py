from typing import Optional
import asyncio 
from app.data.database import usuarios
from fastapi import APIRouter

routerV= APIRouter(
    tags=['Inicio']
)

#otros endpoints
@routerV.get("/")
async def holaMundo():
    return {"mensaje":"Hola Mundo FASTAPI"}

@routerV.get("/v1/Bienvenidos")
async def Bienvenidos():
    return {"mensaje":"Bienvenidos"}

@routerV.get("/v1/Promedio")
async def promedio():
    await asyncio.sleep(3) #simulacion de peticion, consultaBD...
    return {
        "Calificacion":"10",
        "estatus":"200"
    }

@routerV.get("/v1/parametroO/{id}")
async def consultaUno(id:int):
    await asyncio.sleep(3) 
    return {
        "Resultado":"usuario encontrado",
        "Estatus":"200",
        }
    
@routerV.get("/v1/usuario_op/")
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Usuario encontrado":id, "Datos":usuario}
            return {"Mensaje":"Usuario no encontrado"}
        else:
            return { "Aviso":"No se proporciono Id"}
     