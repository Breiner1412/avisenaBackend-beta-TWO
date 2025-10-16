from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.registro_sensores import RegistroSensorCreate, RegistroSensorOut, RegistroSensorUpdate
from app.crud import registro_sensores as crud_registro_sensores

router = APIRouter()
modulo = 3  # ID del módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_registro(registro: RegistroSensorCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_registro_sensores.create_registro(db, registro)
    return {"message": "Registro de sensor creado correctamente"}

@router.get("/by-id/{id_registro}", response_model=RegistroSensorOut)
def obtener_registro(id_registro: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    registro = crud_registro_sensores.get_registro_by_id(db, id_registro)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@router.get("/all", response_model=List[RegistroSensorOut])
def listar_registros(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_registro_sensores.get_all_registros(db)

@router.put("/by-id/{id_registro}")
def actualizar_registro(id_registro: int, registro: RegistroSensorUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_registro_sensores.update_registro_by_id(db, id_registro, registro)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el registro")
    return {"message": "Registro de sensor actualizado correctamente"}
