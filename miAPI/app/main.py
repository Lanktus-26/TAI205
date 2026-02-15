#1. importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional
import asyncio 


#2. inicializacion APP
app= FastAPI(
    title='Mi primer API',
    description='Gerardo Joshua Piña Rivera',
    version='1.0.0' 
    )

#Base de datos ficticia para pruebas:
usuarios=[
    {"id":"1","nombre":"Gerardo","edad":"20"},
    {"id":"2","nombre":"Yazmin","edad":"20"},
    {"id":"3","nombre":"Roberto","edad":"20"},
]

#3. endpoints
@app.get("/",tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Hola Mundo FASTAPI"}

@app.get("/v1/Bienvenidos", tags=['Inicio'])
async def Bienvenidos():
    return {"mensaje":"Bienvenidos"}

@app.get("/v1/Promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3) #simulacion de peticion, consultaBD...
    return {
        "Calificacion":"10",
        "estatus":"200"
    }

@app.get("/v1/parametroO/{id}",tags=['Parametros'])
async def consultaUno(id:int):
    await asyncio.sleep(3) 
    return {
        "Resultado":"usuario encontrado",
        "Estatus":"200",
        }
    
@app.get("/v1/usuario_op/",tags=['Parametro Opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Usuario encontrado":id, "Datos":usuario}
            return {"Mensaje":"Usuario no encontrado"}
        else:
            return { "Aviso":"No se proporciono Id"}
     
   
@app.get("/v1/usuarios/",tags=['CRUD HTTP'])
async def consultar():
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
        
    }
  
@app.post("/v1/usuarios/",tags=['CRUD HTTP'])
async def crear_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado correctamente",
        "status":"200",
        "ususario":usuario
    }
    
@app.put("/v1/usuarios/", tags=["CRUD HTTP"])
async def actualizar_usuario(id:str, usuario:dict):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario["id"] = id
            usuarios[i] = usuario
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/", tags=["CRUD HTTP"])
async def eliminar_usuario(id:str):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(i)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "status": "200",
                "usuario": eliminado
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
