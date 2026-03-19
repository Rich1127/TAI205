            
#1. Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios

#2. Inicializacion APP
app= FastAPI(
    title="Mi primer API", 
    description="Jesus Ricardo Velazquez Morales",
    version="1.0.0"
)
app.include_router(usuarios.routerU)
app.include_router(varios.routerV)

