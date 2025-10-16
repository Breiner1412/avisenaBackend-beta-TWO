from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.detalle_salvamento import DetalleSalvamentoCreate, DetalleSalvamentoUpdate

logger = logging.getLogger(__name__)

def create_detalle(db: Session, detalle: DetalleSalvamentoCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO detalle_salvamento (
                id_producto, id_salvamento, cantidad,
                id_venta, valor_descuento, precio_venta
            ) VALUES (
                :id_producto, :id_salvamento, :cantidad,
                :id_venta, :valor_descuento, :precio_venta
            )
        """)
        db.execute(sentencia, detalle.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear detalle de salvamento: {e}")
        raise Exception("Error de base de datos al crear el detalle de salvamento")

def get_detalle_by_id(db: Session, id_detalle: int):
    try:
        query = text("""
            SELECT id_detalle, id_producto, id_salvamento, cantidad,
                   id_venta, valor_descuento, precio_venta
            FROM detalle_salvamento
            WHERE id_detalle = :id_detalle
        """)
        return db.execute(query, {"id_detalle": id_detalle}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener detalle por id: {e}")
        raise Exception("Error de base de datos al obtener el detalle de salvamento")

def get_all_detalles(db: Session):
    try:
        query = text("""
            SELECT id_detalle, id_producto, id_salvamento, cantidad,
                   id_venta, valor_descuento, precio_venta
            FROM detalle_salvamento
            ORDER BY id_detalle DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar detalles de salvamento: {e}")
        raise Exception("Error de base de datos al listar los detalles")

def update_detalle_by_id(db: Session, id_detalle: int, detalle: DetalleSalvamentoUpdate) -> Optional[bool]:
    try:
        data = detalle.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
        sentencia = text(f"""
            UPDATE detalle_salvamento
            SET {set_clause}
            WHERE id_detalle = :id_detalle
        """)
        data["id_detalle"] = id_detalle
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar detalle {id_detalle}: {e}")
        raise Exception("Error de base de datos al actualizar el detalle de salvamento")
