#1. importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios

#2. inicializacion APP
app= FastAPI(
    title='Mi primer API',
    description='Gerardo Joshua Piña Rivera',
    version='1.0.0' 
    )

app.include_router(usuarios.routerU)
app.include_router(varios.routerV)
