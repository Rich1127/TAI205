
#1. Importaciones
from fastapi import FastAPI
from typing import Optional
import asyncio

#2. Inicializacion APP
app= FastAPI(
    title="Mi primer API", 
    description="Jesus Ricardo Velazquez Morales",
    version="1.0.0"
    )

#BD ficticia
usuarios=[
    {"id":1, "nombre":"Jesus", "edad":20},
    {"id":2, "nombre":"Osiel", "edad":23},
    {"id":3, "nombre":"Yisus", "edad":22},
]
#3. Endpoints
@app.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@app.get("/v1/bienvenidos", tags=['Bienvenidos'])
async def bien():
    return {"mensaje":'Bienvenidos'}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3) #peticion, consultaBD...
    return {"Calificacion":"7.5",
            "estatus":"200"
            }
    
@app.get("/v1/usuario/{id}", tags=['Parametros'])
async def cosultaUno(id:int):
    await asyncio.sleep(3)
    return {"Resultado":"Usuario encontrado",
            "Estatus":"200",
            }

    