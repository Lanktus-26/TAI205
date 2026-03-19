from fastapi import status,HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

routerU= APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

@routerU.get("/")
async def consultar():
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
        
    }
#enpoint modificaco para usar pydantic  
@routerU.post("/",status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
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
  
@routerU.put("/{id}",status_code=status.HTTP_200_OK)
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

@routerU.delete("/{id}",status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:str,userAuth:str=Depends(verificar_peticion)):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(i)
            return {
                "mensaje":f"Elimiado por {userAuth}",
                "status": "200",
                "usuario": eliminado
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
