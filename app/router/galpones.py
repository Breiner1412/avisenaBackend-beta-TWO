from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.galpones import GalponCreate, GalponOut, GalponUpdate
from app.crud import galpones as crud_galpones

router = APIRouter()
modulo = 3  # ID del módulo original

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_galpon(galpon: GalponCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        crud_galpones.create_galpon(db, galpon)
        return {"message": "Galpón creado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-id/{id_galpon}", response_model=GalponOut)
def obtener_galpon(id_galpon: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        galpon = crud_galpones.get_galpon_by_id(db, id_galpon)
        if not galpon:
            raise HTTPException(status_code=404, detail="Galpón no encontrado")
        return galpon
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=List[GalponOut])
def listar_galpones(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        return crud_galpones.get_all_galpones(db)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/by-id/{id_galpon}")
def actualizar_galpon(id_galpon: int, galpon: GalponUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        success = crud_galpones.update_galpon_by_id(db, id_galpon, galpon)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el galpón")
        return {"message": "Galpón actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
