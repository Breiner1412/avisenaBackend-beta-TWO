from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.tipo_gallinas import TipoGallinaCreate, TipoGallinaOut, TipoGallinaUpdate
from app.crud import tipo_gallinas as crud_tipo_gallinas

router = APIRouter()
modulo = 3  # ID del módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_tipo_gallina(data: TipoGallinaCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_tipo_gallinas.create_tipo_gallina(db, data)
    return {"message": "Tipo de gallina creado correctamente"}

@router.get("/by-id/{id_tipo_gallinas}", response_model=TipoGallinaOut)
def obtener_tipo_gallina(id_tipo_gallinas: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    item = crud_tipo_gallinas.get_tipo_gallina_by_id(db, id_tipo_gallinas)
    if not item:
        raise HTTPException(status_code=404, detail="Tipo de gallina no encontrado")
    return item

@router.get("/all", response_model=List[TipoGallinaOut])
def listar_tipos_gallina(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_tipo_gallinas.get_all_tipo_gallinas(db)

@router.put("/by-id/{id_tipo_gallinas}")
def actualizar_tipo_gallina(id_tipo_gallinas: int, data: TipoGallinaUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_tipo_gallinas.update_tipo_gallina_by_id(db, id_tipo_gallinas, data)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el registro")
    return {"message": "Tipo de gallina actualizado correctamente"}
