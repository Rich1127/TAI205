#Modelo de validacion pydantic
from pydantic import BaseModel,Field

class crear_usuario(BaseModel):
    nombre:str = Field(..., min_length=3, max_length=50, description="Juanita")
    edad:int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")

