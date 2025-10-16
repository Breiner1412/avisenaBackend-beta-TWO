# app/crud/users.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from core.security import get_hashed_password
from app.schemas.users import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


def create_user(db: Session, user: UserCreate) -> Optional[bool]:
    try:
        # Encriptar contraseña con passlib centralizado
        pass_encript = get_hashed_password(user.pass_hash)
        user.pass_hash = pass_encript

        sentencia = text(
            """
            INSERT INTO usuarios (
                nombre, id_rol, email,
                telefono, documento,
                pass_hash, estado
            ) VALUES (
                :nombre, :id_rol, :email,
                :telefono, :documento,
                :pass_hash, :estado
            )
            """
        )
        db.execute(sentencia, user.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al crear el usuario")


def get_user_by_email_for_login(db: Session, email: str):
    try:
        query = text(
            """
            SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol, pass_hash
            FROM usuarios INNER JOIN roles ON usuarios.id_rol = roles.id_rol
            WHERE email = :correo
            """
        )
        return db.execute(query, {"correo": email}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por email: {e}")
        raise Exception("Error de base de datos al obtener el usuario")


def get_user_by_email(db: Session, email: str):
    try:
        query = text(
            """
            SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol
            FROM usuarios INNER JOIN roles ON usuarios.id_rol = roles.id_rol
            WHERE email = :correo
            """
        )
        return db.execute(query, {"correo": email}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por email: {e}")
        raise Exception("Error de base de datos al obtener el usuario")


def get_user_by_id(db: Session, id: int):
    try:
        query = text(
            """
            SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol
            FROM usuarios INNER JOIN roles ON usuarios.id_rol = roles.id_rol
            WHERE id_usuario = :id_user
            """
        )
        return db.execute(query, {"id_user": id}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por id: {e}")
        raise Exception("Error de base de datos al obtener el usuario")


def get_all_users(db: Session):
    try:
        query = text(
            """
            SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol
            FROM usuarios INNER JOIN roles ON usuarios.id_rol = roles.id_rol
            ORDER BY id_usuario DESC
            """
        )
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuarios: {e}")
        raise Exception("Error de base de datos al obtener los usuarios")


def get_all_user_except_admins(db: Session):
    try:
        query = text(
            """
            SELECT id_usuario, nombre, documento, usuarios.id_rol, email, telefono, estado, nombre_rol
            FROM usuarios INNER JOIN roles ON usuarios.id_rol = roles.id_rol
            WHERE usuarios.id_rol NOT IN (1,2)
            ORDER BY id_usuario DESC
            """
        )
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuarios: {e}")
        raise Exception("Error de base de datos al obtener los usuarios")


def update_user_by_id(db: Session, user_id: int, user: UserUpdate) -> Optional[bool]:
    try:
        # Solo los campos enviados por el cliente
        user_data = user.model_dump(exclude_unset=True)
        if not user_data:
            return False

        # Si envían pass_hash, lo encriptamos
        if "pass_hash" in user_data and user_data["pass_hash"]:
            user_data["pass_hash"] = get_hashed_password(user_data["pass_hash"])

        # Construir dinámicamente la sentencia UPDATE
        set_clauses = ", ".join([f"{key} = :{key}" for key in user_data.keys()])
        sentencia = text(
            f"""
            UPDATE usuarios
            SET {set_clauses}
            WHERE id_usuario = :id_usuario
            """
        )

        user_data["id_usuario"] = user_id
        result = db.execute(sentencia, user_data)
        db.commit()

        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario {user_id}: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")


def toggle_estado_user(db: Session, user_id: int) -> bool:
    """Borrado lógico: alterna estado TRUE/FALSE"""
    try:
        query = text(
            """
            UPDATE usuarios
            SET estado = NOT estado
            WHERE id_usuario = :id_usuario
            """
        )
        result = db.execute(query, {"id_usuario": user_id})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al cambiar estado del usuario {user_id}: {e}")
        raise Exception("Error de base de datos al actualizar estado del usuario")