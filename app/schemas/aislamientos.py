# app/schemas/aislamientos.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AislamientoBase(BaseModel):
    id_incidente_gallina: int
    fecha_hora: datetime
    id_galpon: int

class AislamientoCreate(AislamientoBase):
    pass

class AislamientoUpdate(BaseModel):
    id_incidente_gallina: Optional[int] = None
    fecha_hora: Optional[datetime] = None
    id_galpon: Optional[int] = None

class AislamientoOut(AislamientoBase):
    id_aislamiento: int
