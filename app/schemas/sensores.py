from pydantic import BaseModel, Field
from typing import Optional

class SensorBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=255)
    id_tipo_sensor: int
    id_galpon: int
    descripcion: str = Field(max_length=140)

class SensorCreate(SensorBase):
    pass

class SensorUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=255)
    id_tipo_sensor: Optional[int] = None
    id_galpon: Optional[int] = None
    descripcion: Optional[str] = Field(default=None, max_length=140)

class SensorOut(SensorBase):
    id_sensor: int
