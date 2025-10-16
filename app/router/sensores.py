from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.sensores import SensorCreate, SensorOut, SensorUpdate
from app.crud import sensores as crud_sensores

router = APIRouter()
modulo = 3  # ID del módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_sensor(sensor: SensorCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_sensores.create_sensor(db, sensor)
    return {"message": "Sensor creado correctamente"}

@router.get("/by-id/{id_sensor}", response_model=SensorOut)
def obtener_sensor(id_sensor: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    sensor = crud_sensores.get_sensor_by_id(db, id_sensor)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return sensor

@router.get("/all", response_model=List[SensorOut])
def listar_sensores(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_sensores.get_all_sensores(db)

@router.put("/by-id/{id_sensor}")
def actualizar_sensor(id_sensor: int, sensor: SensorUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_sensores.update_sensor_by_id(db, id_sensor, sensor)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el sensor")
    return {"message": "Sensor actualizado correctamente"}
