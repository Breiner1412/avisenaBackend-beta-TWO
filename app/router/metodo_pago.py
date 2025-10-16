from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.metodo_pago import MetodoPagoCreate, MetodoPagoOut, MetodoPagoUpdate
from app.crud import metodo_pago as crud_metodo_pago

router = APIRouter()
modulo = 2  # ID del módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_metodo(metodo: MetodoPagoCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_metodo_pago.create_metodo(db, metodo)
    return {"message": "Método de pago creado correctamente"}

@router.get("/by-id/{id_tipo}", response_model=MetodoPagoOut)
def obtener_metodo(id_tipo: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    metodo = crud_metodo_pago.get_metodo_by_id(db, id_tipo)
    if not metodo:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    return metodo

@router.get("/all", response_model=List[MetodoPagoOut])
def listar_metodos(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_metodo_pago.get_all_metodos(db)

@router.put("/by-id/{id_tipo}")
def actualizar_metodo(id_tipo: int, metodo: MetodoPagoUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_metodo_pago.update_metodo_by_id(db, id_tipo, metodo)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el método de pago")
    return {"message": "Método de pago actualizado correctamente"}

@router.put("/cambiar-estado/{id_tipo}")
def cambiar_estado_metodo(id_tipo: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_metodo_pago.toggle_estado_metodo(db, id_tipo)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo cambiar el estado del método de pago")
    return {"message": "Estado del método de pago actualizado correctamente"}
