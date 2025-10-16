from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.tareas import TareaCreate, TareaOut, TareaUpdate
from app.crud import tareas as crud_tareas

router = APIRouter()
modulo = 3  # ID del módulo de tareas

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_tareas.create_tarea(db, tarea)
    return {"message": "Tarea creada correctamente"}

@router.get("/by-id/{id_tarea}", response_model=TareaOut)
def obtener_tarea(id_tarea: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    tarea = crud_tareas.get_tarea_by_id(db, id_tarea)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@router.get("/all", response_model=List[TareaOut])
def listar_tareas(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_tareas.get_all_tareas(db)

@router.put("/by-id/{id_tarea}")
def actualizar_tarea(id_tarea: int, tarea: TareaUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_tareas.update_tarea_by_id(db, id_tarea, tarea)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la tarea")
    return {"message": "Tarea actualizada correctamente"}
