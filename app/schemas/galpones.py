from pydantic import BaseModel, Field
from typing import Optional

class GalponBase(BaseModel):
    id_finca: int
    nombre: str = Field(min_length=2, max_length=30)
    capacidad: int
    cant_actual: int

class GalponCreate(GalponBase):
    pass

class GalponUpdate(BaseModel):
    id_finca: Optional[int] = None
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=30)
    capacidad: Optional[int] = None
    cant_actual: Optional[int] = None

class GalponOut(GalponBase):
    id_galpon: int
