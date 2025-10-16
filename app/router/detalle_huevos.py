from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.detalle_huevos import DetalleHuevosCreate, DetalleHuevosOut, DetalleHuevosUpdate
from app.crud import detalle_huevos as crud_detalle_huevos

router = APIRouter()
modulo = 2  # ID de módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_detalle(detalle: DetalleHuevosCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        crud_detalle_huevos.create_detalle(db, detalle)
        return {"message": "Detalle creado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-id/{id_detalle}", response_model=DetalleHuevosOut)
def obtener_detalle(id_detalle: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        detalle = crud_detalle_huevos.get_detalle_by_id(db, id_detalle)
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        return detalle
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=List[DetalleHuevosOut])
def listar_detalles(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        return crud_detalle_huevos.get_all_detalles(db)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/by-id/{id_detalle}")
def actualizar_detalle(id_detalle: int, detalle: DetalleHuevosUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        success = crud_detalle_huevos.update_detalle_by_id(db, id_detalle, detalle)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el detalle")
        return {"message": "Detalle actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
