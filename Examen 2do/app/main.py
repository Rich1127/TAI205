#Importaciones
from fastapi import FastAPI,status,HTTPException,Depends
from operator import index 
from typing import Optional
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Inicializacion de la App
app= FastAPI(
    title="API examen 2do parcial", 
    description="Jesus Ricardo Velazquez Morales",
    version="1.0.0"
    )

#BD ficticia
reservas=[
    {"id":1, "huesped":"Jesus", "fecha_entrada":"2026-03-01", "tipo_habitacion":"simple", "checkin":"pendiente"},
    {"id":2, "huesped":"Osiel", "fecha_entrada":"2026-05-02", "tipo_habitacion":"doble", "checkin":"pendiente"},
    {"id":3, "huesped":"Yisus", "fecha_entrada":"2026-14-03", "tipo_habitacion":"suite", "checkin":"pendiente"},
]

#Modelo de validacion añade que las validaciones de que la fecha de entrada no pueden ser menores a la fecha actual,
# que la fecha de salida sea mayor a la fecha de entrada y que el estancia no sea mayor a 7
class crear_reserva(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de reserva")
    huesped:str = Field(..., min_length=5, max_length=50, description="Nombre del huesped")
    fecha_entrada:str = Field(..., description="Fecha de entrada")
    tipo_habitacion:str = Field(..., description="Tipo de habitacion")
    fecha_salida:int = Field(..., ge=1, le=31, description="Dia de salida valido entre 1 y 31")
    estancia:Optional[int] = Field(None, gt=0, description="Dias de estancia")
    
#Seguridad HTTP BASIC

seguridad = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "hotel")
    passAuth = secrets.compare_digest(credenciales.password, "r2026")
    
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )
    return credenciales.username

#Endpoints
#Mensaje de inicio
@app.get("/", tags=['Inicio'])
async def reserva_hotel():
    return {"mensaje":"API de reservas de hotel"}

#Crear reserva
@app.post("/v1/reservas/{id}", tags=['CRUD HTTP'])
async def crear_reserva(id: int,userAuth: str = Depends(verificar_peticion)):
    for index, res in enumerate(reservas):
        if res["id"] == id:
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    reservas.insert(index, {"id": id, "huesped": "", "fecha_entrada": "", "tipo_habitacion": "", "fecha_salida": 0, "estancia": 0})
    return{
        "mensaje":"reserva agregada correctamente",
        "status":"200",
        "reserva":{"id": id, "huesped": "", "fecha_entrada": "", "tipo_habitacion": "", "fecha_salida": 0, "estancia": 0}
    }

#Listar reservas
@app.get("/v1/reservas/", tags=['CRUD HTTP'])
async def listar_reservas():
    return reservas

#Consultar reserva
@app.get("/v1/reservas/{id}", tags=['Parametro opcional'])
async def consultar_reserva(id:int):
    await asyncio.sleep(2)
    for reserva in reservas:
        if reserva["id"]==id:
            return {"Reserva encontrada":id,"Datos":reserva}
    return {"Resultado":"Reserva encontrada"}

#Confirmar reserva
@app.put("/v1/reservas/{id}/confirmar", tags=['Parametro opcional'])
async def confirmar_reserva(id:int):
    for reserva in reservas:
        if reserva["id"]==id:
            reserva["estado"]="check-in realizado"
            return {"Check-in realizado con exito", f"El id de la reserva es {id}"}
    return {"Resultado":"Reserva no encontrada"}

#Eliminar reserva
@app.delete("/v1/reservas/{id}/eliminar", tags=['Parametro opcional'])
async def cancelar_reserva(id:int,userAuth: str = Depends(verificar_peticion)):
    for index, reserva in enumerate(reservas):
        if reserva["id"]==id:
            reservas.pop(index)
            return {"Reserva eliminada por": userAuth}
    return {"Resultado":"Reserva no encontrada"}

