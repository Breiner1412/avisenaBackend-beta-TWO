from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.tipo_sensores import TipoSensorCreate, TipoSensorUpdate

logger = logging.getLogger(__name__)

def create_tipo_sensor(db: Session, data: TipoSensorCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO tipo_sensores (nombre, descripcion, modelo)
            VALUES (:nombre, :descripcion, :modelo)
        """)
        db.execute(sentencia, data.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear tipo de sensor: {e}")
        raise Exception("Error de base de datos al crear tipo de sensor")

def get_tipo_sensor_by_id(db: Session, id_tipo: int):
    try:
        query = text("""
            SELECT id_tipo, nombre, descripcion, modelo
            FROM tipo_sensores
            WHERE id_tipo = :id_tipo
        """)
        return db.execute(query, {"id_tipo": id_tipo}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener tipo de sensor: {e}")
        raise Exception("Error de base de datos al obtener tipo de sensor")

def get_all_tipo_sensores(db: Session):
    try:
        query = text("""
            SELECT id_tipo, nombre, descripcion, modelo
            FROM tipo_sensores
            ORDER BY id_tipo DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar tipos de sensores: {e}")
        raise Exception("Error de base de datos al listar tipos de sensores")

def update_tipo_sensor_by_id(db: Session, id_tipo: int, data: TipoSensorUpdate) -> Optional[bool]:
    try:
        valores = data.model_dump(exclude_unset=True)
        if not valores:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in valores.keys()])
        sentencia = text(f"""
            UPDATE tipo_sensores
            SET {set_clause}
            WHERE id_tipo = :id_tipo
        """)
        valores["id_tipo"] = id_tipo
        result = db.execute(sentencia, valores)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar tipo de sensor {id_tipo}: {e}")
        raise Exception("Error de base de datos al actualizar tipo de sensor")
