from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.tareas import TareaCreate, TareaUpdate

logger = logging.getLogger(__name__)

def create_tarea(db: Session, tarea: TareaCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO tareas (id_usuario, descripcion, fecha_hora_init, estado, fecha_hora_fin)
            VALUES (:id_usuario, :descripcion, :fecha_hora_init, :estado, :fecha_hora_fin)
        """)
        db.execute(sentencia, tarea.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear tarea: {e}")
        raise Exception("Error de base de datos al crear la tarea")

def get_tarea_by_id(db: Session, id_tarea: int):
    try:
        query = text("""
            SELECT id_tarea, id_usuario, descripcion, fecha_hora_init, estado, fecha_hora_fin
            FROM tareas
            WHERE id_tarea = :id_tarea
        """)
        return db.execute(query, {"id_tarea": id_tarea}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener tarea por ID: {e}")
        raise Exception("Error de base de datos al obtener la tarea")

def get_all_tareas(db: Session):
    try:
        query = text("""
            SELECT id_tarea, id_usuario, descripcion, fecha_hora_init, estado, fecha_hora_fin
            FROM tareas
            ORDER BY id_tarea DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar tareas: {e}")
        raise Exception("Error de base de datos al listar tareas")

def update_tarea_by_id(db: Session, id_tarea: int, tarea: TareaUpdate) -> Optional[bool]:
    try:
        data = tarea.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
        sentencia = text(f"""
            UPDATE tareas
            SET {set_clause}
            WHERE id_tarea = :id_tarea
        """)
        data["id_tarea"] = id_tarea
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar tarea {id_tarea}: {e}")
        raise Exception("Error de base de datos al actualizar la tarea")
