from pydantic import BaseModel, Field
from typing import Optional

class TipoGallinaBase(BaseModel):
    raza: str = Field(min_length=2, max_length=30)
    descripcion: str = Field(max_length=100)

class TipoGallinaCreate(TipoGallinaBase):
    pass

class TipoGallinaUpdate(BaseModel):
    raza: Optional[str] = Field(default=None, min_length=2, max_length=30)
    descripcion: Optional[str] = Field(default=None, max_length=100)

class TipoGallinaOut(TipoGallinaBase):
    id_tipo_gallinas: int
