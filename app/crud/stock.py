from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.stock import StockCreate, StockUpdate

logger = logging.getLogger(__name__)

def create_stock(db: Session, stock: StockCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO stock (unidad_medida, id_produccion, cantidad_disponible)
            VALUES (:unidad_medida, :id_produccion, :cantidad_disponible)
        """)
        db.execute(sentencia, stock.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear stock: {e}")
        raise Exception("Error de base de datos al crear el registro de stock")

def get_stock_by_id(db: Session, id_producto: int):
    try:
        query = text("""
            SELECT id_producto, unidad_medida, id_produccion, cantidad_disponible
            FROM stock
            WHERE id_producto = :id_producto
        """)
        return db.execute(query, {"id_producto": id_producto}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener stock por ID: {e}")
        raise Exception("Error de base de datos al obtener el registro de stock")

def get_all_stock(db: Session):
    try:
        query = text("""
            SELECT id_producto, unidad_medida, id_produccion, cantidad_disponible
            FROM stock
            ORDER BY id_producto DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar stock: {e}")
        raise Exception("Error de base de datos al listar el stock")

def update_stock_by_id(db: Session, id_producto: int, stock: StockUpdate) -> Optional[bool]:
    try:
        data = stock.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
        sentencia = text(f"""
            UPDATE stock
            SET {set_clause}
            WHERE id_producto = :id_producto
        """)
        data["id_producto"] = id_producto
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar stock {id_producto}: {e}")
        raise Exception("Error de base de datos al actualizar el registro de stock")
