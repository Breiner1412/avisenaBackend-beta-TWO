from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.produccion_huevos import ProduccionHuevosCreate, ProduccionHuevosUpdate

logger = logging.getLogger(__name__)

def create_produccion(db: Session, produccion: ProduccionHuevosCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO produccion_huevos (id_galpon, cantidad, fecha, id_tipo_huevo)
            VALUES (:id_galpon, :cantidad, :fecha, :id_tipo_huevo)
        """)
        db.execute(sentencia, produccion.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al registrar producción: {e}")
        raise Exception("Error de base de datos al registrar producción")

def get_produccion_by_id(db: Session, id_produccion: int):
    try:
        query = text("""
            SELECT id_produccion, id_galpon, cantidad, fecha, id_tipo_huevo
            FROM produccion_huevos
            WHERE id_produccion = :id_produccion
        """)
        return db.execute(query, {"id_produccion": id_produccion}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener producción por ID: {e}")
        raise Exception("Error de base de datos al obtener producción")

def get_all_producciones(db: Session):
    try:
        query = text("""
            SELECT id_produccion, id_galpon, cantidad, fecha, id_tipo_huevo
            FROM produccion_huevos
            ORDER BY id_produccion DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar producciones: {e}")
        raise Exception("Error de base de datos al listar producciones")

def update_produccion_by_id(db: Session, id_produccion: int, produccion: ProduccionHuevosUpdate) -> Optional[bool]:
    try:
        data = produccion.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        sentencia = text(f"""
            UPDATE produccion_huevos
            SET {set_clause}
            WHERE id_produccion = :id_produccion
        """)
        data["id_produccion"] = id_produccion
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar producción {id_produccion}: {e}")
        raise Exception("Error de base de datos al actualizar producción")
