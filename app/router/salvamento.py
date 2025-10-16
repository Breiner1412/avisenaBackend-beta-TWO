from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.salvamento import SalvamentoCreate, SalvamentoOut, SalvamentoUpdate
from app.crud import salvamento as crud_salvamento

router = APIRouter()
modulo = 3  # ID del módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_salvamento(data: SalvamentoCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_salvamento.create_salvamento(db, data)
    return {"message": "Salvamento registrado correctamente"}

@router.get("/by-id/{id_salvamento}", response_model=SalvamentoOut)
def obtener_salvamento(id_salvamento: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    salvamento = crud_salvamento.get_salvamento_by_id(db, id_salvamento)
    if not salvamento:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return salvamento

@router.get("/all", response_model=List[SalvamentoOut])
def listar_salvamentos(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_salvamento.get_all_salvamentos(db)

@router.put("/by-id/{id_salvamento}")
def actualizar_salvamento(id_salvamento: int, data: SalvamentoUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_salvamento.update_salvamento_by_id(db, id_salvamento, data)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el registro")
    return {"message": "Registro actualizado correctamente"}
