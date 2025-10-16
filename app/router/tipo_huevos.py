from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.tipo_huevos import TipoHuevoCreate, TipoHuevoOut, TipoHuevoUpdate
from app.crud import tipo_huevos as crud_tipo_huevos

router = APIRouter()
modulo = 3  # ID del módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_tipo_huevo(data: TipoHuevoCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_tipo_huevos.create_tipo_huevo(db, data)
    return {"message": "Tipo de huevo creado correctamente"}

@router.get("/by-id/{id_tipo_huevo}", response_model=TipoHuevoOut)
def obtener_tipo_huevo(id_tipo_huevo: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    tipo_huevo = crud_tipo_huevos.get_tipo_huevo_by_id(db, id_tipo_huevo)
    if not tipo_huevo:
        raise HTTPException(status_code=404, detail="Tipo de huevo no encontrado")
    return tipo_huevo

@router.get("/all", response_model=List[TipoHuevoOut])
def listar_tipos_huevo(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_tipo_huevos.get_all_tipo_huevos(db)

@router.put("/by-id/{id_tipo_huevo}")
def actualizar_tipo_huevo(id_tipo_huevo: int, data: TipoHuevoUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_tipo_huevos.update_tipo_huevo_by_id(db, id_tipo_huevo, data)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el registro")
    return {"message": "Tipo de huevo actualizado correctamente"}
