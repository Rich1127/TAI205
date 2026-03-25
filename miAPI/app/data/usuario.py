from sqlalchemy import column, Integer, String
from app.data.db import Base

class usuario(Base):
    __tablename__ = "tb-usuarios"

    id = column(Integer,primary_key=True,index=True)
    nombre = column(String)
    edad = column(Integer)