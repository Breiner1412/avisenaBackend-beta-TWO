from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.stock import StockCreate, StockOut, StockUpdate
from app.crud import stock as crud_stock

router = APIRouter()
modulo = 4  # ID del módulo Stock

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_stock(stock: StockCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_stock.create_stock(db, stock)
    return {"message": "Registro de stock creado correctamente"}

@router.get("/by-id/{id_producto}", response_model=StockOut)
def obtener_stock(id_producto: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    stock = crud_stock.get_stock_by_id(db, id_producto)
    if not stock:
        raise HTTPException(status_code=404, detail="Registro de stock no encontrado")
    return stock

@router.get("/all", response_model=List[StockOut])
def listar_stock(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_stock.get_all_stock(db)

@router.put("/by-id/{id_producto}")
def actualizar_stock(id_producto: int, stock: StockUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_stock.update_stock_by_id(db, id_producto, stock)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el registro de stock")
    return {"message": "Registro de stock actualizado correctamente"}
