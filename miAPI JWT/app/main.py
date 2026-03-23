            
#1. Importaciones
from operator import index

from fastapi import FastAPI,status,HTTPException,Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timedelta
import secrets

#2. Inicializacion APP
app= FastAPI(
    title="Mi primer API", 
    description="Jesus Ricardo Velazquez Morales",
    version="1.0.0"
    )

# Configuraciones OAuth2 + JWT
SECRET_KEY = "your-secret-key-here"  # En producción, usar una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#BD ficticia
usuarios=[
    {"id":1, "nombre":"Jesus", "edad":20, "username": "jesus", "hashed_password": bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')},
    {"id":2, "nombre":"Osiel", "edad":23, "username": "osiel", "hashed_password": bcrypt.hashpw("password2".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')},
    {"id":3, "nombre":"Yisus", "edad":22, "username": "yisus", "hashed_password": bcrypt.hashpw("password3".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')},
]

#Modelo de validacion pydantic
class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario")
    nombre:str = Field(..., min_length=3, max_length=50, description="Juanita")
    edad:int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Funciones de autenticación
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_user(username: str):
    for user in usuarios:
        if user["username"] == username:
            return user
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token, tags=['Autenticación'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

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
    
@app.get("/v1/parametro0/{id}", tags=['Parametros'])
async def cosultaUno(id:int):
    await asyncio.sleep(3)
    return {"Resultado":"Usuario encontrado",
            "Estatus":"200",
            }

@app.get("/v1/parametro1/", tags=['Parametro opcional'])
async def cosultaOP(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Resultado":"Usuario encontrado"}
    else:
         return {"Aviso":"No se proporciono id"}
     
     
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def cosultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
    
@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"usuario agregado correctamente",
        "usuario":usuario
    }
    
@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario_actualizado: dict, current_user: dict = Depends(get_current_user)):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario_actualizado.get("nombre", usr["nombre"])
            usr["edad"] = usuario_actualizado.get("edad", usr["edad"])
            
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usr
            }
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int, current_user: dict = Depends(get_current_user)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            index = usuarios.index(usr)
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {current_user['username']}",
                "status": "200",
                "usuario_eliminado": usr
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")