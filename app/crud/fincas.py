# app/crud/fincas.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.fincas import FincaCreate, FincaUpdate

logger = logging.getLogger(__name__)

def create_finca(db: Session, finca: FincaCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO fincas (nombre, longitud, latitud, estado)
            VALUES (:nombre, :longitud, :latitud, :estado)
        """)
        db.execute(sentencia, finca.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear finca: {e}")
        raise Exception("Error de base de datos al crear la finca")

def get_finca_by_id(db: Session, id_finca: int):
    try:
        query = text("""
            SELECT id_finca, nombre, longitud, latitud, estado
            FROM fincas
            WHERE id_finca = :id_finca
        """)
        return db.execute(query, {"id_finca": id_finca}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener finca por id: {e}")
        raise Exception("Error de base de datos al obtener la finca")

def get_all_fincas(db: Session):
    try:
        query = text("""
            SELECT id_finca, nombre, longitud, latitud, estado
            FROM fincas
            ORDER BY id_finca DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener fincas: {e}")
        raise Exception("Error de base de datos al obtener las fincas")

def update_finca_by_id(db: Session, id_finca: int, finca: FincaUpdate) -> Optional[bool]:
    try:
        finca_data = finca.model_dump(exclude_unset=True)
        if not finca_data:
            return False

        set_clauses = ", ".join([f"{key} = :{key}" for key in finca_data.keys()])
        sentencia = text(f"""
            UPDATE fincas SET {set_clauses}
            WHERE id_finca = :id_finca
        """)
        finca_data["id_finca"] = id_finca
        result = db.execute(sentencia, finca_data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar finca {id_finca}: {e}")
        raise Exception("Error de base de datos al actualizar la finca")

def toggle_estado_finca(db: Session, id_finca: int) -> bool:
    try:
        query = text("""
            UPDATE fincas SET estado = NOT estado WHERE id_finca = :id_finca
        """)
        result = db.execute(query, {"id_finca": id_finca})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al cambiar estado de la finca {id_finca}: {e}")
        raise Exception("Error de base de datos al cambiar estado de la finca")

