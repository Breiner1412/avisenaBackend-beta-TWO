from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.produccion_huevos import ProduccionHuevosCreate, ProduccionHuevosOut, ProduccionHuevosUpdate
from app.crud import produccion_huevos as crud_produccion_huevos

router = APIRouter()
modulo = 3  # ID del módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_produccion(produccion: ProduccionHuevosCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_produccion_huevos.create_produccion(db, produccion)
    return {"message": "Producción registrada correctamente"}

@router.get("/by-id/{id_produccion}", response_model=ProduccionHuevosOut)
def obtener_produccion(id_produccion: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    produccion = crud_produccion_huevos.get_produccion_by_id(db, id_produccion)
    if not produccion:
        raise HTTPException(status_code=404, detail="Producción no encontrada")
    return produccion

@router.get("/all", response_model=List[ProduccionHuevosOut])
def listar_producciones(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_produccion_huevos.get_all_producciones(db)

@router.put("/by-id/{id_produccion}")
def actualizar_produccion(id_produccion: int, produccion: ProduccionHuevosUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_produccion_huevos.update_produccion_by_id(db, id_produccion, produccion)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la producción")
    return {"message": "Producción actualizada correctamente"}
