from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.tipo_gallinas import TipoGallinaCreate, TipoGallinaUpdate

logger = logging.getLogger(__name__)

def create_tipo_gallina(db: Session, data: TipoGallinaCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO tipo_gallinas (raza, descripcion)
            VALUES (:raza, :descripcion)
        """)
        db.execute(sentencia, data.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear tipo de gallina: {e}")
        raise Exception("Error de base de datos al crear tipo de gallina")

def get_tipo_gallina_by_id(db: Session, id_tipo_gallinas: int):
    try:
        query = text("""
            SELECT id_tipo_gallinas, raza, descripcion
            FROM tipo_gallinas
            WHERE id_tipo_gallinas = :id_tipo_gallinas
        """)
        return db.execute(query, {"id_tipo_gallinas": id_tipo_gallinas}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener tipo de gallina: {e}")
        raise Exception("Error de base de datos al obtener tipo de gallina")

def get_all_tipo_gallinas(db: Session):
    try:
        query = text("""
            SELECT id_tipo_gallinas, raza, descripcion
            FROM tipo_gallinas
            ORDER BY id_tipo_gallinas DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar tipos de gallinas: {e}")
        raise Exception("Error de base de datos al listar tipos de gallinas")

def update_tipo_gallina_by_id(db: Session, id_tipo_gallinas: int, data: TipoGallinaUpdate) -> Optional[bool]:
    try:
        valores = data.model_dump(exclude_unset=True)
        if not valores:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in valores.keys()])
        sentencia = text(f"""
            UPDATE tipo_gallinas
            SET {set_clause}
            WHERE id_tipo_gallinas = :id_tipo_gallinas
        """)
        valores["id_tipo_gallinas"] = id_tipo_gallinas
        result = db.execute(sentencia, valores)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar tipo de gallina {id_tipo_gallinas}: {e}")
        raise Exception("Error de base de datos al actualizar tipo de gallina")
