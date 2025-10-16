from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.galpones import GalponCreate, GalponUpdate

logger = logging.getLogger(__name__)

def create_galpon(db: Session, galpon: GalponCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO galpones (id_finca, nombre, capacidad, cant_actual)
            VALUES (:id_finca, :nombre, :capacidad, :cant_actual)
        """)
        db.execute(sentencia, galpon.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear galpón: {e}")
        raise Exception("Error de base de datos al crear el galpón")

def get_galpon_by_id(db: Session, id_galpon: int):
    try:
        query = text("""
            SELECT id_galpon, id_finca, nombre, capacidad, cant_actual
            FROM galpones
            WHERE id_galpon = :id_galpon
        """)
        return db.execute(query, {"id_galpon": id_galpon}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener galpón por id: {e}")
        raise Exception("Error de base de datos al obtener el galpón")

def get_all_galpones(db: Session):
    try:
        query = text("""
            SELECT id_galpon, id_finca, nombre, capacidad, cant_actual
            FROM galpones
            ORDER BY id_galpon DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener galpones: {e}")
        raise Exception("Error de base de datos al obtener los galpones")

def update_galpon_by_id(db: Session, id_galpon: int, galpon: GalponUpdate) -> Optional[bool]:
    try:
        data = galpon.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        sentencia = text(f"""
            UPDATE galpones SET {set_clause}
            WHERE id_galpon = :id_galpon
        """)
        data["id_galpon"] = id_galpon
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar galpón {id_galpon}: {e}")
        raise Exception("Error de base de datos al actualizar el galpón")
