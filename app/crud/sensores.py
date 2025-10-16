from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.sensores import SensorCreate, SensorUpdate

logger = logging.getLogger(__name__)

def create_sensor(db: Session, sensor: SensorCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO sensores (nombre, id_tipo_sensor, id_galpon, descripcion)
            VALUES (:nombre, :id_tipo_sensor, :id_galpon, :descripcion)
        """)
        db.execute(sentencia, sensor.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear sensor: {e}")
        raise Exception("Error de base de datos al crear sensor")

def get_sensor_by_id(db: Session, id_sensor: int):
    try:
        query = text("""
            SELECT id_sensor, nombre, id_tipo_sensor, id_galpon, descripcion
            FROM sensores
            WHERE id_sensor = :id_sensor
        """)
        return db.execute(query, {"id_sensor": id_sensor}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener sensor por ID: {e}")
        raise Exception("Error de base de datos al obtener sensor")

def get_all_sensores(db: Session):
    try:
        query = text("""
            SELECT id_sensor, nombre, id_tipo_sensor, id_galpon, descripcion
            FROM sensores
            ORDER BY id_sensor DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar sensores: {e}")
        raise Exception("Error de base de datos al listar sensores")

def update_sensor_by_id(db: Session, id_sensor: int, sensor: SensorUpdate) -> Optional[bool]:
    try:
        data = sensor.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        sentencia = text(f"""
            UPDATE sensores
            SET {set_clause}
            WHERE id_sensor = :id_sensor
        """)
        data["id_sensor"] = id_sensor
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar sensor {id_sensor}: {e}")
        raise Exception("Error de base de datos al actualizar sensor")
