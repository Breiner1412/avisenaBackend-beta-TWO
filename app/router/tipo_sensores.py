from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.tipo_sensores import TipoSensorCreate, TipoSensorOut, TipoSensorUpdate
from app.crud import tipo_sensores as crud_tipo_sensores

router = APIRouter()
modulo = 3  # ID del módulo Tipo Sensores

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_tipo_sensor(data: TipoSensorCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_tipo_sensores.create_tipo_sensor(db, data)
    return {"message": "Tipo de sensor creado correctamente"}

@router.get("/by-id/{id_tipo}", response_model=TipoSensorOut)
def obtener_tipo_sensor(id_tipo: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    tipo = crud_tipo_sensores.get_tipo_sensor_by_id(db, id_tipo)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de sensor no encontrado")
    return tipo

@router.get("/all", response_model=List[TipoSensorOut])
def listar_tipo_sensores(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_tipo_sensores.get_all_tipo_sensores(db)

@router.put("/by-id/{id_tipo}")
def actualizar_tipo_sensor(id_tipo: int, data: TipoSensorUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_tipo_sensores.update_tipo_sensor_by_id(db, id_tipo, data)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el registro")
    return {"message": "Tipo de sensor actualizado correctamente"}
