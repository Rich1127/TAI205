from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

routerV= APIRouter(tags=['Inicio'])

#3. Endpoints
@routerV.get("/")
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@routerV.get("/v1/bienvenidos")
async def bien():
    return {"mensaje":'Bienvenidos'}

@routerV.get("/v1/promedio")
async def promedio():
    await asyncio.sleep(3) #peticion, consultaBD...
    return {"Calificacion":"7.5",
            "estatus":"200"
            }
    
@routerV.get("/v1/parametro0/{id}")
async def cosultaUno(id:int):
    await asyncio.sleep(3)
    return {"Resultado":"Usuario encontrado",
            "Estatus":"200",
            }

@routerV.get("/v1/parametro1/")
async def cosultaOP(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Resultado":"Usuario encontrado"}
    else:
         return {"Aviso":"No se proporciono id"}