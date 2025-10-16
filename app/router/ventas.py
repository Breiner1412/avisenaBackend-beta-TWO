from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.ventas import VentaCreate, VentaOut, VentaUpdate
from app.crud import ventas as crud_ventas

router = APIRouter()
modulo = 2  # ID del módulo Ventas

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_venta(data: VentaCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_ventas.create_venta(db, data)
    return {"message": "Venta registrada correctamente"}

@router.get("/by-id/{id_venta}", response_model=VentaOut)
def obtener_venta(id_venta: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    venta = crud_ventas.get_venta_by_id(db, id_venta)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@router.get("/all", response_model=List[VentaOut])
def listar_ventas(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_ventas.get_all_ventas(db)

@router.put("/by-id/{id_venta}")
def actualizar_venta(id_venta: int, data: VentaUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_ventas.update_venta_by_id(db, id_venta, data)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la venta")
    return {"message": "Venta actualizada correctamente"}
