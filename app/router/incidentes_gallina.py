from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.incidentes_gallina import IncidenteGallinaCreate, IncidenteGallinaOut, IncidenteGallinaUpdate
from app.crud import incidentes_gallina as crud_incidentes

router = APIRouter()
modulo = 3  # ID del módulo

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def crear_incidente(incidente: IncidenteGallinaCreate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "insertar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    crud_incidentes.create_incidente(db, incidente)
    return {"message": "Incidente creado correctamente"}

@router.get("/by-id/{id_inc_gallina}", response_model=IncidenteGallinaOut)
def obtener_incidente(id_inc_gallina: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    incidente = crud_incidentes.get_incidente_by_id(db, id_inc_gallina)
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    return incidente

@router.get("/all", response_model=List[IncidenteGallinaOut])
def listar_incidentes(db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "seleccionar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    return crud_incidentes.get_all_incidentes(db)

@router.put("/by-id/{id_inc_gallina}")
def actualizar_incidente(id_inc_gallina: int, incidente: IncidenteGallinaUpdate, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_incidentes.update_incidente_by_id(db, id_inc_gallina, incidente)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el incidente")
    return {"message": "Incidente actualizado correctamente"}

@router.put("/cambiar-estado/{id_inc_gallina}")
def cambiar_estado(id_inc_gallina: int, db: Session = Depends(get_db), user_token = Depends(get_current_user)):
    if not verify_permissions(db, user_token.id_rol, modulo, "actualizar"):
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    success = crud_incidentes.cambiar_estado_incidente(db, id_inc_gallina)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo cambiar el estado del incidente")
    return {"message": "Estado del incidente actualizado correctamente"}
