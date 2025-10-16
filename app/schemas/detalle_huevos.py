from pydantic import BaseModel, Field
from typing import Optional

class DetalleHuevosBase(BaseModel):
    id_producto: int
    cantidad: int
    id_venta: int
    valor_descuento: float
    precio_venta: float

class DetalleHuevosCreate(DetalleHuevosBase):
    pass

class DetalleHuevosUpdate(BaseModel):
    id_producto: Optional[int] = None
    cantidad: Optional[int] = None
    id_venta: Optional[int] = None
    valor_descuento: Optional[float] = None
    precio_venta: Optional[float] = None

class DetalleHuevosOut(DetalleHuevosBase):
    id_detalle: int
