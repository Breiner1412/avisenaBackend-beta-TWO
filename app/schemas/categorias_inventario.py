from pydantic import BaseModel, Field
from typing import Optional

class CategoriaInventarioBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=30)
    descripcion: Optional[str] = Field(default=None, max_length=255)

class CategoriaInventarioCreate(CategoriaInventarioBase):
    pass

class CategoriaInventarioUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=30)
    descripcion: Optional[str] = Field(default=None, max_length=255)

class CategoriaInventarioOut(CategoriaInventarioBase):
    id_categoria: int
