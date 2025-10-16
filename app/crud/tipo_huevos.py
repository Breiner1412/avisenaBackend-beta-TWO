from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.tipo_huevos import TipoHuevoCreate, TipoHuevoUpdate

logger = logging.getLogger(__name__)

def create_tipo_huevo(db: Session, data: TipoHuevoCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO tipo_huevos (color, tamano)
            VALUES (:color, :tamano)
        """)
        db.execute(sentencia, data.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear tipo de huevo: {e}")
        raise Exception("Error de base de datos al crear tipo de huevo")

def get_tipo_huevo_by_id(db: Session, id_tipo_huevo: int):
    try:
        query = text("""
            SELECT id_tipo_huevo, color, tamano
            FROM tipo_huevos
            WHERE id_tipo_huevo = :id_tipo_huevo
        """)
        return db.execute(query, {"id_tipo_huevo": id_tipo_huevo}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener tipo de huevo por ID: {e}")
        raise Exception("Error de base de datos al obtener tipo de huevo")

def get_all_tipo_huevos(db: Session):
    try:
        query = text("""
            SELECT id_tipo_huevo, color, tamano
            FROM tipo_huevos
            ORDER BY id_tipo_huevo DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar tipos de huevos: {e}")
        raise Exception("Error de base de datos al listar tipos de huevos")

def update_tipo_huevo_by_id(db: Session, id_tipo_huevo: int, data: TipoHuevoUpdate) -> Optional[bool]:
    try:
        valores = data.model_dump(exclude_unset=True)
        if not valores:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in valores.keys()])
        sentencia = text(f"""
            UPDATE tipo_huevos
            SET {set_clause}
            WHERE id_tipo_huevo = :id_tipo_huevo
        """)
        valores["id_tipo_huevo"] = id_tipo_huevo
        result = db.execute(sentencia, valores)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar tipo de huevo {id_tipo_huevo}: {e}")
        raise Exception("Error de base de datos al actualizar tipo de huevo")
