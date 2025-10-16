from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.metodo_pago import MetodoPagoCreate, MetodoPagoUpdate

logger = logging.getLogger(__name__)

def create_metodo(db: Session, metodo: MetodoPagoCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO metodo_pago (nombre, descripcion, estado)
            VALUES (:nombre, :descripcion, :estado)
        """)
        db.execute(sentencia, metodo.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear método de pago: {e}")
        raise Exception("Error de base de datos al crear método de pago")

def get_metodo_by_id(db: Session, id_tipo: int):
    try:
        query = text("""
            SELECT id_tipo, nombre, descripcion, estado
            FROM metodo_pago
            WHERE id_tipo = :id_tipo
        """)
        return db.execute(query, {"id_tipo": id_tipo}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener método por id: {e}")
        raise Exception("Error de base de datos al obtener método de pago")

def get_all_metodos(db: Session):
    try:
        query = text("""
            SELECT id_tipo, nombre, descripcion, estado
            FROM metodo_pago
            ORDER BY id_tipo DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar métodos: {e}")
        raise Exception("Error de base de datos al listar métodos de pago")

def update_metodo_by_id(db: Session, id_tipo: int, metodo: MetodoPagoUpdate) -> Optional[bool]:
    try:
        data = metodo.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        sentencia = text(f"""
            UPDATE metodo_pago SET {set_clause}
            WHERE id_tipo = :id_tipo
        """)
        data["id_tipo"] = id_tipo
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar método {id_tipo}: {e}")
        raise Exception("Error de base de datos al actualizar método de pago")

def toggle_estado_metodo(db: Session, id_tipo: int) -> bool:
    try:
        query = text("""
            UPDATE metodo_pago SET estado = NOT estado WHERE id_tipo = :id_tipo
        """)
        result = db.execute(query, {"id_tipo": id_tipo})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al cambiar estado del método {id_tipo}: {e}")
        raise Exception("Error de base de datos al cambiar estado del método de pago")
