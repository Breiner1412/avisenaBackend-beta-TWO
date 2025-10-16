from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.incidentes_gallina import IncidenteGallinaCreate, IncidenteGallinaUpdate

logger = logging.getLogger(__name__)

def create_incidente(db: Session, incidente: IncidenteGallinaCreate) -> bool:
    try:
        sentencia = text("""
            INSERT INTO incidentes_gallina (
                galpon_origen, tipo_incidente, cantidad,
                descripcion, fecha_hora, esta_resuelto
            ) VALUES (
                :galpon_origen, :tipo_incidente, :cantidad,
                :descripcion, :fecha_hora, :esta_resuelto
            )
        """)
        db.execute(sentencia, incidente.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear incidente de gallina: {e}")
        raise Exception("Error de base de datos al crear incidente")

def get_incidente_by_id(db: Session, id_inc_gallina: int):
    try:
        query = text("""
            SELECT id_inc_gallina, galpon_origen, tipo_incidente, cantidad,
                   descripcion, fecha_hora, esta_resuelto
            FROM incidentes_gallina
            WHERE id_inc_gallina = :id_inc_gallina
        """)
        return db.execute(query, {"id_inc_gallina": id_inc_gallina}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener incidente por id: {e}")
        raise Exception("Error de base de datos al obtener incidente")

def get_all_incidentes(db: Session):
    try:
        query = text("""
            SELECT id_inc_gallina, galpon_origen, tipo_incidente, cantidad,
                   descripcion, fecha_hora, esta_resuelto
            FROM incidentes_gallina
            ORDER BY id_inc_gallina DESC
        """)
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al listar incidentes: {e}")
        raise Exception("Error de base de datos al listar incidentes")

def update_incidente_by_id(db: Session, id_inc_gallina: int, incidente: IncidenteGallinaUpdate) -> Optional[bool]:
    try:
        data = incidente.model_dump(exclude_unset=True)
        if not data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        sentencia = text(f"""
            UPDATE incidentes_gallina SET {set_clause}
            WHERE id_inc_gallina = :id_inc_gallina
        """)
        data["id_inc_gallina"] = id_inc_gallina
        result = db.execute(sentencia, data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar incidente {id_inc_gallina}: {e}")
        raise Exception("Error de base de datos al actualizar incidente")

def cambiar_estado_incidente(db: Session, id_inc_gallina: int) -> Optional[bool]:
    try:
        sentencia = text("""
            UPDATE incidentes_gallina
            SET esta_resuelto = NOT esta_resuelto
            WHERE id_inc_gallina = :id_inc_gallina
        """)
        result = db.execute(sentencia, {"id_inc_gallina": id_inc_gallina})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al cambiar estado del incidente {id_inc_gallina}: {e}")
        raise Exception("Error de base de datos al cambiar estado del incidente")
