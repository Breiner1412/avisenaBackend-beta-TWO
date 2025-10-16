from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.categorias_inventario import CategoriaInventarioCreate, CategoriaInventarioOut, CategoriaInventarioUpdate
from app.crud import categorias_inventario as crud_categorias

router = APIRouter()
modulo = 4  # ID de módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_categoria(categoria: CategoriaInventarioCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        crud_categorias.create_categoria(db, categoria)
        return {"message": "Categoría creada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-id/{id_categoria}", response_model=CategoriaInventarioOut)
def get_categoria(id_categoria: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        categoria = crud_categorias.get_categoria_by_id(db, id_categoria)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return categoria
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=List[CategoriaInventarioOut])
def get_all_categorias(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        return crud_categorias.get_all_categorias(db)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/by-id/{id_categoria}")
def update_categoria(id_categoria: int, categoria: CategoriaInventarioUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    try:
        if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        success = crud_categorias.update_categoria_by_id(db, id_categoria, categoria)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la categoría")
        return {"message": "Categoría actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
