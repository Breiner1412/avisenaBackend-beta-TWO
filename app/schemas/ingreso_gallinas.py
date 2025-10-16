from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class IngresoGallinasBase(BaseModel):
    id_galpon: int
    fecha: date
    id_tipo_gallina: int
    cantidad_gallinas: int = Field(gt=0)

class IngresoGallinasCreate(IngresoGallinasBase):
    pass

class IngresoGallinasUpdate(BaseModel):
    id_galpon: Optional[int] = None
    fecha: Optional[date] = None
    id_tipo_gallina: Optional[int] = None
    cantidad_gallinas: Optional[int] = Field(default=None, gt=0)

class IngresoGallinasOut(IngresoGallinasBase):
    id_ingreso: int
