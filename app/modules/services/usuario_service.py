from flask import abort
import sqlite3
from app.modules.db.db import get_connection
from app.modules.services.auditoria_service import registrar_accion
from werkzeug.security import check_password_hash, generate_password_hash


def cambiar_rol(actor, objetivo_id, nuevo_rol):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if actor["id"] == objetivo_id:
            return None, "No puedes modificarte a ti mismo."

        usuario_objetivo = cursor.execute(
            "SELECT * FROM usuarios WHERE id = ?", (objetivo_id,)
        ).fetchone()

        if not usuario_objetivo:
            return None, "Usuario no encontrado"

        if usuario_objetivo["rol"] == nuevo_rol:
            return None, "Este usuario ya tiene ese rol."

        cursor.execute(
            "UPDATE usuarios SET rol = ? WHERE id = ?",
            (nuevo_rol, objetivo_id)
        )
        conn.commit()

        registrar_accion(
            actor_id=actor["id"],
            accion="CAMBIAR_ROL",
            objetivo_id=objetivo_id,
            entidad="usuario",
            descripcion=f"{usuario_objetivo['rol']} → {nuevo_rol}"
        )

        return True, None
    finally:
        cursor.close()
        conn.close()

def crear_usuario(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "El usuario ya existe"
    finally:
        cursor.close()
        conn.close()

def obtener_usuario(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        return cursor.execute(
            "SELECT * FROM usuarios WHERE username = ?",
            (username,)
        ).fetchone()
    finally:
        cursor.close()
        conn.close()

def login(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        usuario = cursor.execute(
            "SELECT * FROM usuarios WHERE username = ?",
            (username,)
        ).fetchone()

        if not usuario:
            return None

        if check_password_hash(usuario["password"], password):
            return usuario

        return None
    finally:
        cursor.close()
        conn.close()

def obtener_perfil(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        return cursor.execute(
            "SELECT * FROM usuarios WHERE id = ?", (id,)
        ).fetchone()
    finally:
        cursor.close()
        conn.close()