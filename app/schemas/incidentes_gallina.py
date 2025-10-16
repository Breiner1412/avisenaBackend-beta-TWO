from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class IncidenteGallinaBase(BaseModel):
    galpon_origen: int
    tipo_incidente: str = Field(max_length=50)
    cantidad: int
    descripcion: str = Field(max_length=255)
    fecha_hora: datetime
    esta_resuelto: bool

class IncidenteGallinaCreate(IncidenteGallinaBase):
    pass

class IncidenteGallinaUpdate(BaseModel):
    galpon_origen: Optional[int] = None
    tipo_incidente: Optional[str] = Field(default=None, max_length=50)
    cantidad: Optional[int] = None
    descripcion: Optional[str] = Field(default=None, max_length=255)
    fecha_hora: Optional[datetime] = None
    esta_resuelto: Optional[bool] = None

class IncidenteGallinaOut(IncidenteGallinaBase):
    id_inc_gallina: int
