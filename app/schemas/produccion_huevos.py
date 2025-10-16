from pydantic import BaseModel
from datetime import date
from typing import Optional

class ProduccionHuevosBase(BaseModel):
    id_galpon: int
    cantidad: int
    fecha: date
    id_tipo_huevo: int

class ProduccionHuevosCreate(ProduccionHuevosBase):
    pass

class ProduccionHuevosUpdate(BaseModel):
    id_galpon: Optional[int] = None
    cantidad: Optional[int] = None
    fecha: Optional[date] = None
    id_tipo_huevo: Optional[int] = None

class ProduccionHuevosOut(ProduccionHuevosBase):
    id_produccion: int
