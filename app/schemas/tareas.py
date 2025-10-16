from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TareaBase(BaseModel):
    id_usuario: int
    descripcion: str = Field(max_length=180)
    fecha_hora_init: datetime
    estado: str  # Enum: Asignada, Pendiente, En proceso, Completada, Cancelada
    fecha_hora_fin: datetime

class TareaCreate(TareaBase):
    pass

class TareaUpdate(BaseModel):
    id_usuario: Optional[int] = None
    descripcion: Optional[str] = Field(default=None, max_length=180)
    fecha_hora_init: Optional[datetime] = None
    estado: Optional[str] = None
    fecha_hora_fin: Optional[datetime] = None

class TareaOut(TareaBase):
    id_tarea: int
