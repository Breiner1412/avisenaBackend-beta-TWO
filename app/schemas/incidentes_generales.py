from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class IncidenteGeneralBase(BaseModel):
    descripcion: str = Field(max_length=255)
    fecha_hora: datetime
    id_finca: int
    esta_resuelta: bool

class IncidenteGeneralCreate(IncidenteGeneralBase):
    pass

class IncidenteGeneralUpdate(BaseModel):
    descripcion: Optional[str] = Field(default=None, max_length=255)
    fecha_hora: Optional[datetime] = None
    id_finca: Optional[int] = None
    esta_resuelta: Optional[bool] = None

class IncidenteGeneralOut(IncidenteGeneralBase):
    id_incidente: int
