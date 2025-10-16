from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.salvamento import SalvamentoCreate, SalvamentoUpdate

logger = logging.getLogger(__name__)

def create_salvamento(db: Session, data: SalvamentoCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO salvamento (id_galpon, fecha, id_tipo_gallina, cantidad_gallinas)
            VALUES (:id_galpon, :fecha, :id_tipo_gallina, :cantidad_gallinas)
        """)
        db.execute(sentencia, data.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear salvamento: {e}")
        raise Exception("Error de base de datos al crear registro de salvamento")

def get_salvamento_by_id(db: Session, id_salvamento: int):
    try:
        query = text("""
            SELECT id_salvamento, id_galpon, fecha, id_tipo_gallina, cantidad_gallinas
            FROM salvamento
            WHERE id_salvamento = :id_salvamento
        """)
        return db.execute(query, {"id_salvamento": id_salvamento}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener salvamento por ID: {e}")
        raise Exception("Error de base de datos al obtener registro")

def get_all_salvamentos(db: Session):
    try:
        query = text("""
            SELECT id_salvamento, id_galpon, fecha, id_tipo_gallina, cantidad_gallinas
            FROM salvamento
            ORDER BY id_salvamento DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar salvamentos: {e}")
        raise Exception("Error de base de datos al listar registros")

def update_salvamento_by_id(db: Session, id_salvamento: int, data: SalvamentoUpdate) -> Optional[bool]:
    try:
        payload = data.model_dump(exclude_unset=True)
        if not payload:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in payload.keys()])
        sentencia = text(f"""
            UPDATE salvamento
            SET {set_clause}
            WHERE id_salvamento = :id_salvamento
        """)
        payload["id_salvamento"] = id_salvamento
        result = db.execute(sentencia, payload)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar salvamento {id_salvamento}: {e}")
        raise Exception("Error de base de datos al actualizar registro")
