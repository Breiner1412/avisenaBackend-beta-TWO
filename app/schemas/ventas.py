from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VentaBase(BaseModel):
    fecha_hora: datetime
    id_usuario: int
    tipo_pago: int
    total: float

class VentaCreate(VentaBase):
    pass

class VentaUpdate(BaseModel):
    fecha_hora: Optional[datetime] = None
    id_usuario: Optional[int] = None
    tipo_pago: Optional[int] = None
    total: Optional[float] = None

class VentaOut(VentaBase):
    id_venta: int
