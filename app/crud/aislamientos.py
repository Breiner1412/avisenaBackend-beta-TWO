# app/crud/aislamientos.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.aislamientos import AislamientoCreate, AislamientoUpdate

logger = logging.getLogger(__name__)

def create_aislamiento(db: Session, aislamiento: AislamientoCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO aislamiento (id_incidente_gallina, fecha_hora, id_galpon)
            VALUES (:id_incidente_gallina, :fecha_hora, :id_galpon)
        """)
        db.execute(sentencia, aislamiento.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear aislamiento: {e}")
        raise Exception("Error de base de datos al crear el aislamiento")

def get_aislamiento_by_id(db: Session, id_aislamiento: int):
    try:
        query = text("""
            SELECT id_aislamiento, id_incidente_gallina, fecha_hora, id_galpon
            FROM aislamiento
            WHERE id_aislamiento = :id_aislamiento
        """)
        return db.execute(query, {"id_aislamiento": id_aislamiento}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener aislamiento por id: {e}")
        raise Exception("Error de base de datos al obtener el aislamiento")

def get_all_aislamientos(db: Session):
    try:
        query = text("""
            SELECT id_aislamiento, id_incidente_gallina, fecha_hora, id_galpon
            FROM aislamiento
            ORDER BY id_aislamiento DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener aislamientos: {e}")
        raise Exception("Error de base de datos al obtener los aislamientos")

def update_aislamiento_by_id(db: Session, id_aislamiento: int, aislamiento: AislamientoUpdate) -> Optional[bool]:
    try:
        data = aislamiento.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
        sentencia = text(f"""
            UPDATE aislamiento SET {set_clause}
            WHERE id_aislamiento = :id_aislamiento
        """)
        data["id_aislamiento"] = id_aislamiento
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar aislamiento {id_aislamiento}: {e}")
        raise Exception("Error de base de datos al actualizar el aislamiento")
