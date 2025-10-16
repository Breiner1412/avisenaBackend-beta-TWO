# app/schemas/users.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=70)
    id_rol: int
    email: EmailStr
    telefono: str = Field(min_length=7, max_length=15)
    documento: str = Field(min_length=8, max_length=20)
    estado: bool


class UserCreate(UserBase):
    pass_hash: str = Field(min_length=8)


class UserUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=70)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(default=None, min_length=7, max_length=15)
    documento: Optional[str] = Field(default=None, min_length=8, max_length=20)
    id_rol: Optional[int] = None
    # Nota: El cambio de contraseña se maneja en un endpoint dedicado si lo prefieres
    pass_hash: Optional[str] = Field(default=None, min_length=8)


class UserOut(UserBase):
    id_usuario: int
    nombre_rol: str
