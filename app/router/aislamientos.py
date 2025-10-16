# app/router/aislamientos.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.aislamientos import AislamientoCreate, AislamientoOut, AislamientoUpdate
from app.crud import aislamientos as crud_aislamientos

router = APIRouter()
modulo = 3

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_aislamiento(aislamiento: AislamientoCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        crud_aislamientos.create_aislamiento(db, aislamiento)
        return {"message": "Aislamiento creado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-id/{id_aislamiento}", response_model=AislamientoOut)
def get_aislamiento(id_aislamiento: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        aislamiento = crud_aislamientos.get_aislamiento_by_id(db, id_aislamiento)
        if not aislamiento:
            raise HTTPException(status_code=404, detail="Aislamiento no encontrado")
        return aislamiento
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=List[AislamientoOut])
def get_all_aislamientos(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        return crud_aislamientos.get_all_aislamientos(db)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/by-id/{id_aislamiento}")
def update_aislamiento(id_aislamiento: int, aislamiento: AislamientoUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        success = crud_aislamientos.update_aislamiento_by_id(db, id_aislamiento, aislamiento)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el aislamiento")
        return {"message": "Aislamiento actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
