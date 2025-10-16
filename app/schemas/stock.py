from pydantic import BaseModel
from typing import Optional

class StockBase(BaseModel):
    unidad_medida: str
    id_produccion: int
    cantidad_disponible: int

class StockCreate(StockBase):
    pass

class StockUpdate(BaseModel):
    unidad_medida: Optional[str] = None
    id_produccion: Optional[int] = None
    cantidad_disponible: Optional[int] = None

class StockOut(StockBase):
    id_producto: int
