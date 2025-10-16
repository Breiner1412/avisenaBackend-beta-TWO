from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.ingreso_gallinas import IngresoGallinasCreate, IngresoGallinasUpdate

logger = logging.getLogger(__name__)

def create_ingreso(db: Session, ingreso: IngresoGallinasCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO ingreso_gallinas (id_galpon, fecha, id_tipo_gallina, cantidad_gallinas)
            VALUES (:id_galpon, :fecha, :id_tipo_gallina, :cantidad_gallinas)
        """)
        db.execute(sentencia, ingreso.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear ingreso de gallinas: {e}")
        raise Exception("Error de base de datos al crear el ingreso")

def get_ingreso_by_id(db: Session, id_ingreso: int):
    try:
        query = text("""
            SELECT id_ingreso, id_galpon, fecha, id_tipo_gallina, cantidad_gallinas
            FROM ingreso_gallinas
            WHERE id_ingreso = :id_ingreso
        """)
        return db.execute(query, {"id_ingreso": id_ingreso}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener ingreso por id: {e}")
        raise Exception("Error de base de datos al obtener ingreso")

def get_all_ingresos(db: Session):
    try:
        query = text("""
            SELECT id_ingreso, id_galpon, fecha, id_tipo_gallina, cantidad_gallinas
            FROM ingreso_gallinas
            ORDER BY id_ingreso DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar ingresos: {e}")
        raise Exception("Error de base de datos al listar los ingresos")

def update_ingreso_by_id(db: Session, id_ingreso: int, ingreso: IngresoGallinasUpdate) -> Optional[bool]:
    try:
        data = ingreso.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
        sentencia = text(f"""
            UPDATE ingreso_gallinas
            SET {set_clause}
            WHERE id_ingreso = :id_ingreso
        """)
        data["id_ingreso"] = id_ingreso
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar ingreso {id_ingreso}: {e}")
        raise Exception("Error de base de datos al actualizar el ingreso")
