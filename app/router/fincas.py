# app/router/fincas.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.fincas import FincaCreate, FincaOut, FincaUpdate
from app.crud import fincas as crud_fincas

router = APIRouter()
modulo = 4


@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_finca(
    finca: FincaCreate,
    db: Session = Depends(get_db),
    user_token=Depends(get_current_user),
):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        crud_fincas.create_finca(db, finca)
        return {"message": "Finca creada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-id/{id_finca}", response_model=FincaOut)
def get_finca(
    id_finca: int, db: Session = Depends(get_db), user_token=Depends(get_current_user)
):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        finca = crud_fincas.get_finca_by_id(db, id_finca)
        if not finca:
            raise HTTPException(status_code=404, detail="Finca no encontrada")
        return finca
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all", response_model=List[FincaOut])
def get_all_fincas(db: Session = Depends(get_db), user_token=Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        return crud_fincas.get_all_fincas(db)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/by-id/{id_finca}")
def update_finca(
    id_finca: int,
    finca: FincaUpdate,
    db: Session = Depends(get_db),
    user_token=Depends(get_current_user),
):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        success = crud_fincas.update_finca_by_id(db, id_finca, finca)
        if not success:
            raise HTTPException(
                status_code=400, detail="No se pudo actualizar la finca"
            )
        return {"message": "Finca actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/cambiar-estado/{id_finca}")
def cambiar_estado_finca(
    id_finca: int, db: Session = Depends(get_db), user_token=Depends(get_current_user)
):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        actualizado = crud_fincas.toggle_estado_finca(db, id_finca)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Finca no encontrada")
        return {"message": "Estado de la finca cambiado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
