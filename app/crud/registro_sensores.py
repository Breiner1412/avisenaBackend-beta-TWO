from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.registro_sensores import RegistroSensorCreate, RegistroSensorUpdate

logger = logging.getLogger(__name__)

def create_registro(db: Session, registro: RegistroSensorCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO registro_sensores (id_sensor, dato_sensor, fecha_hora, u_medida)
            VALUES (:id_sensor, :dato_sensor, :fecha_hora, :u_medida)
        """)
        db.execute(sentencia, registro.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear registro de sensor: {e}")
        raise Exception("Error de base de datos al crear el registro")

def get_registro_by_id(db: Session, id_registro: int):
    try:
        query = text("""
            SELECT id_registro, id_sensor, dato_sensor, fecha_hora, u_medida
            FROM registro_sensores
            WHERE id_registro = :id_registro
        """)
        return db.execute(query, {"id_registro": id_registro}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener registro por id: {e}")
        raise Exception("Error de base de datos al obtener el registro")

def get_all_registros(db: Session):
    try:
        query = text("""
            SELECT id_registro, id_sensor, dato_sensor, fecha_hora, u_medida
            FROM registro_sensores
            ORDER BY id_registro DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar registros de sensores: {e}")
        raise Exception("Error de base de datos al listar registros")

def update_registro_by_id(db: Session, id_registro: int, registro: RegistroSensorUpdate) -> Optional[bool]:
    try:
        data = registro.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        sentencia = text(f"""
            UPDATE registro_sensores
            SET {set_clause}
            WHERE id_registro = :id_registro
        """)
        data["id_registro"] = id_registro
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar registro {id_registro}: {e}")
        raise Exception("Error de base de datos al actualizar el registro")
