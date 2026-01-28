#1. Importaciones
from fastapi import FastAPI

#2. Inicializacion APP
app= FastAPI()

#3. Endpoints
@app.get("/")
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@app.get("/bienvenidos")
async def bien():
    return {"mensaje":"Bienvenidos"}