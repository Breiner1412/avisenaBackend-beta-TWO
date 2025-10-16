from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.inventario_finca import InventarioFincaCreate, InventarioFincaUpdate

logger = logging.getLogger(__name__)

def create_inventario(db: Session, inventario: InventarioFincaCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO inventario_finca (nombre, cantidad, unidad_medida, descripcion, id_categoria, id_finca)
            VALUES (:nombre, :cantidad, :unidad_medida, :descripcion, :id_categoria, :id_finca)
        """)
        db.execute(sentencia, inventario.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear inventario finca: {e}")
        raise Exception("Error de base de datos al crear el inventario")

def get_inventario_by_id(db: Session, id_inventario: int):
    try:
        query = text("""
            SELECT id_inventario, nombre, cantidad, unidad_medida, descripcion, id_categoria, id_finca
            FROM inventario_finca
            WHERE id_inventario = :id_inventario
        """)
        return db.execute(query, {"id_inventario": id_inventario}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener inventario por id: {e}")
        raise Exception("Error de base de datos al obtener el inventario")

def get_all_inventarios(db: Session):
    try:
        query = text("""
            SELECT id_inventario, nombre, cantidad, unidad_medida, descripcion, id_categoria, id_finca
            FROM inventario_finca
            ORDER BY id_inventario DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar inventarios: {e}")
        raise Exception("Error de base de datos al listar inventarios")

def update_inventario_by_id(db: Session, id_inventario: int, inventario: InventarioFincaUpdate) -> Optional[bool]:
    try:
        data = inventario.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        sentencia = text(f"""
            UPDATE inventario_finca SET {set_clause}
            WHERE id_inventario = :id_inventario
        """)
        data["id_inventario"] = id_inventario
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar inventario {id_inventario}: {e}")
        raise Exception("Error de base de datos al actualizar el inventario")
