from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.ingreso_gallinas import IngresoGallinasCreate, IngresoGallinasOut, IngresoGallinasUpdate
from app.crud import ingreso_gallinas as crud_ingreso_gallinas

router = APIRouter()
modulo = 3  # ID del módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_ingreso(ingreso: IngresoGallinasCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_ingreso_gallinas.create_ingreso(db, ingreso)
    return {"message": "Ingreso registrado correctamente"}

@router.get("/by-id/{id_ingreso}", response_model=IngresoGallinasOut)
def obtener_ingreso(id_ingreso: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    ingreso = crud_ingreso_gallinas.get_ingreso_by_id(db, id_ingreso)
    if not ingreso:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")
    return ingreso

@router.get("/all", response_model=List[IngresoGallinasOut])
def listar_ingresos(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_ingreso_gallinas.get_all_ingresos(db)

@router.put("/by-id/{id_ingreso}")
def actualizar_ingreso(id_ingreso: int, ingreso: IngresoGallinasUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_ingreso_gallinas.update_ingreso_by_id(db, id_ingreso, ingreso)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el ingreso")
    return {"message": "Ingreso actualizado correctamente"}
