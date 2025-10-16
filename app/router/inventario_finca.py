from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.inventario_finca import InventarioFincaCreate, InventarioFincaOut, InventarioFincaUpdate
from app.crud import inventario_finca as crud_inventario

router = APIRouter()
modulo = 4  # ID del módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_inventario(inventario: InventarioFincaCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_inventario.create_inventario(db, inventario)
    return {"message": "Inventario registrado correctamente"}

@router.get("/by-id/{id_inventario}", response_model=InventarioFincaOut)
def obtener_inventario(id_inventario: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    inventario = crud_inventario.get_inventario_by_id(db, id_inventario)
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario

@router.get("/all", response_model=List[InventarioFincaOut])
def listar_inventarios(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_inventario.get_all_inventarios(db)

@router.put("/by-id/{id_inventario}")
def actualizar_inventario(id_inventario: int, inventario: InventarioFincaUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_inventario.update_inventario_by_id(db, id_inventario, inventario)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el inventario")
    return {"message": "Inventario actualizado correctamente"}
