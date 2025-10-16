from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RegistroSensorBase(BaseModel):
    id_sensor: int
    dato_sensor: float
    fecha_hora: datetime
    u_medida: str

class RegistroSensorCreate(RegistroSensorBase):
    pass

class RegistroSensorUpdate(BaseModel):
    id_sensor: Optional[int] = None
    dato_sensor: Optional[float] = None
    fecha_hora: Optional[datetime] = None
    u_medida: Optional[str] = None

class RegistroSensorOut(RegistroSensorBase):
    id_registro: int
