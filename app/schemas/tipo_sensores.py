from pydantic import BaseModel, Field
from typing import Optional

class TipoSensorBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=70)
    descripcion: str = Field(max_length=255)
    modelo: str = Field(min_length=1, max_length=70)

class TipoSensorCreate(TipoSensorBase):
    pass

class TipoSensorUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=70)
    descripcion: Optional[str] = Field(default=None, max_length=255)
    modelo: Optional[str] = Field(default=None, min_length=1, max_length=70)

class TipoSensorOut(TipoSensorBase):
    id_tipo: int
