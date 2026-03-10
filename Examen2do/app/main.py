#importaciones
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

#Reserva de ospedaje

app = FastAPI(title="Reserva de hospedaje", version="1.0.0")

reservas = []

estadosdereserva = {"confirmada"," cancelada"}
tipoh = {"sencilla","doble","suite"}

#Validaciones con pydantic
class Reservas(BaseModel):
    id: int
    #Huesped minimo 5 caracteres
    nombreH: str = Field(..., min_length=5)
    f_entrada: int
    f_salida: int
    t_estancia: int = Field(..., ge=1, le=7, description="Estancia valida entre 1 y 7 dias") 
    tipoh: str
    #validacion nombre
    @field_validator("nombre")
    @classmethod
    def v_nombre(cls, v: str):
        if not re.fullmatch(r"[A-Za-z\s]+", v.strip()):
            raise ValueError("Nombre invalido")
        return v.strip()
    #validacion tipo
    @field_validator("tipoh")
    @classmethod
    def v_tipoh(cls, v: str):
        if v not in tipoh:
            raise ValueError("Tipo de habitacion invalido")
        return v
    #fehca de etrada no menor a fecha actual    
    @field_validator("f_entrada")
    @classmethod
    def v_etd(cls, v: int):
        actual = datetime.now().date
        if v < actual:
            raise ValueError("Fecha invalida")
        return v
    #Fecha de salida no mayor que fecha entrada
    # @field_validator("f_salida")
    # @classmethod
    # def v_sld(cls, v: int):
    #     salida = f_sailda
    #     if v > actual:
    #         raise ValueError("Fecha invalida")
    #     return v
    
class c_reserva(BaseModel):
    Reservas_id: int
    usuario: str


#crear reserva
@app.post("/Reserva", status_code=status.HTTP_201_CREATED)
def crear_reserva(payload: Reservas):
    if any(l["id"] == payload.id for l in Reservas):
        raise HTTPException(status_code=400, detail="La reserva ya existe")
    Reservas.append(payload.model_dump())
    return {"mensaje": "Reserva registrada correctamente"}

#Lista de reservas
@app.get("/Reserva")
def ver_reservas():
    return reservas


@app.get("/Reserva/buscar/{Reservas_id}")
def buscar(texto: str):
    t = texto.lower().strip()
    return [l for l in reservas if t in l["nombre"].lower()]


@app.post("/reservas", status_code=status.HTTP_201_CREATED)
def prestar(payload: c_reserva):
    reserva = next((l for l in reservas if l["id"] == payload.Reservas_id), None)
    if not reserva:
        raise HTTPException(status_code=400, detail="La reserva no existe")
    if reserva["estado"] == "confirmada":
        raise HTTPException(status_code=409, detail="La Reservas ya está reservado")

    reserva["estado"] = "cancelada"
    reservas.append(payload.model_dump())
    return {"mensaje": "Reserva registrada"}
#verificar estados

@app.put("/Reserva/{Reservas_id}/cancelar")
def cancelar(Reservas_id: int):
    reserva = next((l for l in reservas if l["id"] == Reservas_id), None)
    if not reserva:
        raise HTTPException(status_code=400, detail="La reserva no existe")
    if reserva["estado"] == "cancelada":
        raise HTTPException(status_code=409, detail="No hay reservas activas")

    reserva["estado"] = "confirmada"
    return {"mensaje": "Reserva cancelada"}


@app.delete("/Modreservas/{Reservas_id}")
def borrar_reserva(Reservas_id: int):
    p = next((x for x in reservas if x["Reservas_id"] == Reservas_id), None)
    if not p:
        raise HTTPException(status_code=409, detail="La reserva no existe")
    reservas.remove(p)
    return {"mensaje": "Reserva cancelada"}

# protger UnicodeEncodeErrors con usuario y contra: hotel r2026