from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.ventas import VentaCreate, VentaUpdate

logger = logging.getLogger(__name__)

def create_venta(db: Session, data: VentaCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO ventas (fecha_hora, id_usuario, tipo_pago, total)
            VALUES (:fecha_hora, :id_usuario, :tipo_pago, :total)
        """)
        db.execute(sentencia, data.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear venta: {e}")
        raise Exception("Error de base de datos al crear la venta")

def get_venta_by_id(db: Session, id_venta: int):
    try:
        query = text("""
            SELECT id_venta, fecha_hora, id_usuario, tipo_pago, total
            FROM ventas
            WHERE id_venta = :id_venta
        """)
        return db.execute(query, {"id_venta": id_venta}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener venta por ID: {e}")
        raise Exception("Error de base de datos al obtener la venta")

def get_all_ventas(db: Session):
    try:
        query = text("""
            SELECT id_venta, fecha_hora, id_usuario, tipo_pago, total
            FROM ventas
            ORDER BY id_venta DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar ventas: {e}")
        raise Exception("Error de base de datos al listar ventas")

def update_venta_by_id(db: Session, id_venta: int, data: VentaUpdate) -> Optional[bool]:
    try:
        valores = data.model_dump(exclude_unset=True)
        if not valores:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in valores.keys()])
        sentencia = text(f"""
            UPDATE ventas
            SET {set_clause}
            WHERE id_venta = :id_venta
        """)
        valores["id_venta"] = id_venta
        result = db.execute(sentencia, valores)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar venta {id_venta}: {e}")
        raise Exception("Error de base de datos al actualizar venta")
