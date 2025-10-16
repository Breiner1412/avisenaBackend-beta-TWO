from pydantic import BaseModel
from datetime import date
from typing import Optional

class SalvamentoBase(BaseModel):
    id_galpon: int
    fecha: date
    id_tipo_gallina: int
    cantidad_gallinas: int

class SalvamentoCreate(SalvamentoBase):
    pass

class SalvamentoUpdate(BaseModel):
    id_galpon: Optional[int] = None
    fecha: Optional[date] = None
    id_tipo_gallina: Optional[int] = None
    cantidad_gallinas: Optional[int] = None

class SalvamentoOut(SalvamentoBase):
    id_salvamento: int
