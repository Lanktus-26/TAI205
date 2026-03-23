#1. importaciones
from fastapi import FastAPI,status,HTTPException, Depends
from typing import Optional
import asyncio 
from pydantic import BaseModel,Field
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



#2. inicializacion APP
app= FastAPII(
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

class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")
    
#Seguridad OAuth2 + JWT
SECRET_KEY = "lanktus123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

#credenciales de prueba
VALID_USERNAME = "lanktus"
VALID_PASSWORD = "123456"

#creacion del token
def crear_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#verificion
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username != VALID_USERNAME:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o usuario no existe")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado o no es válido")
    return username


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
#enpoint modificaco para usar pydantic  
@app.post("/v1/usuarios/",tags=['CRUD HTTP'],status_code=status.HTTP_201_CREATED)
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
    
# token endpoint (OAuth2)
@app.post("/token", tags=["Autenticación"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == VALID_USERNAME and form_data.password == VALID_PASSWORD:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = crear_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

# endpoints protegidos con OAuth2 JWT
@app.put("/v1/usuarios/", tags=["CRUD HTTP"])
async def actualizar_usuario(id: str, usuario: dict, current_user: str = Depends(verificar_token)):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario["id"] = id
            usuarios[i] = usuario
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usuario,
                "actualizado_por": current_user
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/", tags=["CRUD HTTP"])
async def eliminar_usuario(id: str, current_user: str = Depends(verificar_token)):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(i)
            return {
                "mensaje": f"Eliminado por {current_user}",
                "status": "200",
                "usuario": eliminado
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")