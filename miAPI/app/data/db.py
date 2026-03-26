from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1. Definimos la url de conexión con el contendor
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
    )
#2. Creamos el motor de conexión
engine = create_engine(DATABASE_URL)

#3. Definimos el manejador de sesiones
SessionLocal = sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
    )

#4. Instacionamos la Base delcarativa del modelo
Base = declarative_base()  

#5. Funcion para manejo de sesiones por petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

