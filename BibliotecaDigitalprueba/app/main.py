from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

app = FastAPI(title="Biblioteca Digital", version="1.0.0")

libros = []
prestamos = []

estados_posibles = {"disponible", "prestado"}
añomin = 1450

#validacuioines con pydantic
class Usuario(BaseModel):
    nombre: str
    correo: str

    @field_validator("nombre")
    @classmethod
    def v_nombre(cls, v: str):
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+", v.strip()): #quitar espacios
            raise ValueError("Nombre invalido")
        return v.strip()

    @field_validator("correo")
    @classmethod
    def v_correo(cls, v: str):
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", v.strip()): #pide caracter, @, caracter, punto y caracter
            raise ValueError("Correo invalido")
        return v.strip()


class Libro(BaseModel):
    id: int
    nombre: str = Field(..., min_length=2, max_length=100) #limites del nombre 
    autor: str
    año: int
    paginas: int = Field(..., gt=1)
    estado: str = "disponible"

    @field_validator("estado")
    @classmethod
    def v_estado(cls, v: str):
        if v not in estados_posibles:
            raise ValueError("Estado invalido")
        return v

    @field_validator("año")
    @classmethod
    def v_año(cls, v: int):
        actual = datetime.now().year
        if v <= añomin or v > actual:
            raise ValueError("Año invalido")
        return v


class Prestamo(BaseModel):
    libro_id: int
    usuario: Usuario


@app.post("/libros", status_code=status.HTTP_201_CREATED)
def crear_libro(payload: Libro):
    if any(l["id"] == payload.id for l in libros):
        raise HTTPException(status_code=400, detail="El libro ya existe")
    libros.append(payload.model_dump())
    return {"mensaje": "Libro registrado correctamente"}


@app.get("/libros")
def ver_libros():
    return libros


@app.get("/libros/buscar/{texto}")
def buscar(texto: str):
    t = texto.lower().strip()
    return [l for l in libros if t in l["nombre"].lower()]


@app.post("/prestamos", status_code=status.HTTP_201_CREATED)
def prestar(payload: Prestamo):
    libro = next((l for l in libros if l["id"] == payload.libro_id), None)
    if not libro:
        raise HTTPException(status_code=400, detail="El libro no existe")
    if libro["estado"] == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya está prestado")

    libro["estado"] = "prestado"
    prestamos.append(payload.model_dump())
    return {"mensaje": "Prestamo registrado"}


@app.put("/libros/{libro_id}/devolver")
def devolver(libro_id: int):
    libro = next((l for l in libros if l["id"] == libro_id), None)
    if not libro:
        raise HTTPException(status_code=400, detail="El libro no existe")
    if libro["estado"] == "disponible":
        raise HTTPException(status_code=409, detail="No hay prestamos activo")

    libro["estado"] = "disponible"
    return {"mensaje": "Libro devuelto"}


@app.delete("/prestamos/{libro_id}")
def borrar_prestamo(libro_id: int):
    p = next((x for x in prestamos if x["libro_id"] == libro_id), None)
    if not p:
        raise HTTPException(status_code=409, detail="El prestamo no existe")
    prestamos.remove(p)
    return {"mensaje": "Prestamo eliminado"}