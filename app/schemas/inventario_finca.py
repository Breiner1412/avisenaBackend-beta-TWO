from pydantic import BaseModel, Field
from typing import Optional

class InventarioFincaBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=30)
    cantidad: int
    unidad_medida: str
    descripcion: str = Field(max_length=100)
    id_categoria: int
    id_finca: int

class InventarioFincaCreate(InventarioFincaBase):
    pass

class InventarioFincaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=30)
    cantidad: Optional[int] = None
    unidad_medida: Optional[str] = None
    descripcion: Optional[str] = Field(default=None, max_length=100)
    id_categoria: Optional[int] = None
    id_finca: Optional[int] = None

class InventarioFincaOut(InventarioFincaBase):
    id_inventario: int
