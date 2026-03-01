import requests
API = 'http://localhost:5000/v1/usuarios/'

from flask import Flask, request

app = Flask(__name__)

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
def saludar():
    return "¡Hola desde el endpoint!"   