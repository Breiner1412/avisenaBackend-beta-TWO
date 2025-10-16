# app/schemas/fincas.py
from pydantic import BaseModel, Field
from typing import Optional

class FincaBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=30)
    longitud: float
    latitud: float
    estado: bool

class FincaCreate(FincaBase):
    pass

class FincaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=30)
    longitud: Optional[float] = None
    latitud: Optional[float] = None
    estado: Optional[bool] = None

class FincaOut(FincaBase):
    id_finca: int