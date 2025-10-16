from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.categorias_inventario import CategoriaInventarioCreate, CategoriaInventarioUpdate

logger = logging.getLogger(__name__)

def create_categoria(db: Session, categoria: CategoriaInventarioCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO categoria_inventario (nombre, descripcion)
            VALUES (:nombre, :descripcion)
        """)
        db.execute(sentencia, categoria.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear categoría de inventario: {e}")
        raise Exception("Error de base de datos al crear la categoría")

def get_categoria_by_id(db: Session, id_categoria: int):
    try:
        query = text("""
            SELECT id_categoria, nombre, descripcion
            FROM categoria_inventario
            WHERE id_categoria = :id_categoria
        """)
        return db.execute(query, {"id_categoria": id_categoria}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener categoría por id: {e}")
        raise Exception("Error de base de datos al obtener la categoría")

def get_all_categorias(db: Session):
    try:
        query = text("""
            SELECT id_categoria, nombre, descripcion
            FROM categoria_inventario
            ORDER BY id_categoria DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener categorías: {e}")
        raise Exception("Error de base de datos al obtener las categorías")

def update_categoria_by_id(db: Session, id_categoria: int, categoria: CategoriaInventarioUpdate) -> Optional[bool]:
    try:
        data = categoria.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        sentencia = text(f"""
            UPDATE categoria_inventario
            SET {set_clause}
            WHERE id_categoria = :id_categoria
        """)
        data["id_categoria"] = id_categoria
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar categoría {id_categoria}: {e}")
        raise Exception("Error de base de datos al actualizar la categoría")
