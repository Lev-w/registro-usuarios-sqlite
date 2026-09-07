from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.modules.db.db import get_session
from app.modules.db.models import UsuarioModel
from app.modules.services.auditoria_service import registrar_accion


def cambiar_rol(actor, objetivo_id, nuevo_rol):
    session = get_session()
    try:
        if actor["id"] == objetivo_id:
            return None, "No puedes modificarte a ti mismo."

        usuario_objetivo = session.get(UsuarioModel, objetivo_id)

        if not usuario_objetivo:
            return None, "Usuario no encontrado"

        if usuario_objetivo.rol == nuevo_rol:
            return None, "Este usuario ya tiene ese rol."

        rol_anterior = usuario_objetivo.rol
        usuario_objetivo.rol = nuevo_rol
        session.commit()

        registrar_accion(
            actor_id=actor["id"],
            accion="CAMBIAR_ROL",
            objetivo_id=objetivo_id,
            entidad="usuario",
            descripcion=f"{rol_anterior} → {nuevo_rol}"
        )

        return True, None
    finally:
        session.close()


def crear_usuario(username, password):
    session = get_session()
    try:
        password_hash = generate_password_hash(password)
        session.add(UsuarioModel(username=username, password=password_hash))
        session.commit()
        return True, None
    except IntegrityError:
        session.rollback()
        return False, "El usuario ya existe"
    finally:
        session.close()


def obtener_usuario(username):
    session = get_session()
    try:
        usuario = session.scalar(
            select(UsuarioModel).where(UsuarioModel.username == username)
        )
        return usuario.to_dict() if usuario else None
    finally:
        session.close()


def login(username, password):
    session = get_session()
    try:
        usuario = session.scalar(
            select(UsuarioModel).where(UsuarioModel.username == username)
        )

        if not usuario:
            return None

        if check_password_hash(usuario.password, password):
            return usuario.to_dict()

        return None
    finally:
        session.close()


def obtener_perfil(id):
    session = get_session()
    try:
        usuario = session.get(UsuarioModel, id)
        return usuario.to_dict() if usuario else None
    finally:
        session.close()
