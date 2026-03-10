#importaciones
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

#Reserva de ospedaje

app = FastAPI(title="Reserva de hospedaje", version="1.0.0")

reservas = []
reservasconf = []

estadosp = {"confirmada"," cancelada"}
tipo = {"sencilla","doble","suite"}
#agg año minimo

#Validaciones con pydantic

##Huesped minimo 5 caracteres
class Huesped(BaseModel):
    nombre: str = Field(..., min_length=5)
    
    @field_validator("nombre")
    @classmethod
    def v_nombre(cls, v: str):
        if not re.fullmatch(r"[A-Za-z\s]+", v.strip()):
            raise ValueError("Nombre invalido")
        return v.strip()

class Habitacion(BaseModel):
    id: int
    entrada: int
    salida: int
##Estancia no mayor a 7 dias
    estancia: int = Field(..., ge=1, le=7, description="Estancia valida entre 1 y 7 dias")
    estado: str 
##Tipo de habitacion
    @field_validator("estado")
    @classmethod
    def v_estado(cls, v: str):
        if v not in estadosp:
            raise ValueError("Estado invalido")
        return v
    
##fehca de etrada no menor a fecha actual    
    @field_validator("entrada")
    @classmethod
    def v_etd(cls, v: int):
        actual = datetime.now().year
        if v < actual:
            raise ValueError("Fecha invalida")
        return v
##Fecha de salida no mayor que fecha entrada
#verificar validacion

    # @field_validator("salida")
    # @classmethod
    # def v_sld(cls, v: int):
    #     f = datetime.now().year
    #     if v > v_etd:
    #         raise ValueError("Fecha invalida")
    #     return v
    
class reserva(BaseModel):
    Habitacion_id: int
    usuario: Huesped

#endpoits
#Crear reserva Post
#Listar reserva Get
#Consultar por ID Get
#confirmar reserva Post
#Cancelar reserva Delete


@app.post("/Reserva", status_code=status.HTTP_201_CREATED)
def crear_reserva(payload: Habitacion):
    if any(l["id"] == payload.id for l in Habitacion):
        raise HTTPException(status_code=400, detail="La reserva ya existe")
    Habitacion.append(payload.model_dump())
    return {"mensaje": "Reserva registrada correctamente"}


@app.get("/Reserva")
def ver_reservas():
    return reservas


@app.get("/Reserva/buscar/{texto}")
def buscar(texto: str):
    t = texto.lower().strip()
    return [l for l in reservas if t in l["nombre"].lower()]


@app.post("/reservas", status_code=status.HTTP_201_CREATED)
def prestar(payload: reserva):
    reserva = next((l for l in reservas if l["id"] == payload.Habitacion_id), None)
    if not reserva:
        raise HTTPException(status_code=400, detail="La reserva no existe")
    if reserva["estado"] == "confirmada":
        raise HTTPException(status_code=409, detail="La habitacion ya está reservado")

    reserva["estado"] = "cancelada"
    reservas.append(payload.model_dump())
    return {"mensaje": "Reserva registrada"}
#verificar estados

@app.put("/Reserva/{Habitacion_id}/cancelar")
def cancelar(Habitacion_id: int):
    reserva = next((l for l in reservas if l["id"] == Habitacion_id), None)
    if not reserva:
        raise HTTPException(status_code=400, detail="La reserva no existe")
    if reserva["estado"] == "cancelada":
        raise HTTPException(status_code=409, detail="No hay reservas activas")

    reserva["estado"] = "confirmada"
    return {"mensaje": "Reserva cancelada"}


@app.delete("/Modreservas/{Habitacion_id}")
def borrar_reserva(Habitacion_id: int):
    p = next((x for x in reservas if x["Habitacion_id"] == Habitacion_id), None)
    if not p:
        raise HTTPException(status_code=409, detail="La reserva no existe")
    reservas.remove(p)
    return {"mensaje": "Reserva cancelada"}
    
    