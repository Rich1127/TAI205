#Seguridad HTTP BASIC
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import status,HTTPException,Depends

seguridad = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "Jesus")
    passAuth = secrets.compare_digest(credenciales.password, "123456")
    
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )
    return credenciales.username