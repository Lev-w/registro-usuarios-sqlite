from flask import request, jsonify, Blueprint, session, g, abort
from werkzeug.security import generate_password_hash
from app.helpers import responses
import app.modules.db.db as db
from app.modules.services import auditoria_service
import app.modules.validators as validators
from app.modules.services import usuario_service
import sqlite3
from app.modules.decorators import login_required, roles_required

main = Blueprint("main", __name__)

@main.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.get_json()

    datos, error = validators.validar_usuario(data)

    if error:
        abort(400, description=error)

    ok, error_servicio = usuario_service.crear_usuario(**datos)
    if not ok:
        abort(400, description=error_servicio)

    return jsonify(responses.success_response(mensaje="Usuario agregado.")), 201

@main.route("/login", methods=["POST"])
def login_route():
    data = request.get_json()

    datos, error = validators.validar_login(data)

    if error:
        abort(400, description=error)

    usuario = usuario_service.login(datos["username"], datos["password"])

    if not usuario:
        abort(401, description="Credenciales inválidas")

    session["user_id"] = usuario["id"]
    session["username"] = usuario["username"]
    nombre_formateado = usuario["username"].capitalize()

    return jsonify(responses.success_response(mensaje=f"Login completado. Bienvenido, {nombre_formateado}.")), 200

@main.route("/perfil", methods=["GET"])
@login_required
def ver_mi_perfil():
    return jsonify(responses.success_response(
    data={"id": g.usuario["id"], "username": g.usuario["username"], "rol": g.usuario["rol"]},
    mensaje="Perfil obtenido")), 200

@main.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    auditoria_service.registrar_accion(actor_id=g.usuario["id"], accion="LOGOUT", entidad="usuario")
    return jsonify(responses.success_response(mensaje="Sesion cerrada")), 200

@main.route("/usuarios/<int:id>/rol", methods=["PUT"])
@login_required
@roles_required("admin")
def cambiar_rol(id):
    data = request.get_json()

    nuevo_rol, error = validators.validar_cambio_rol(data)

    if error:
        abort(400, description=error)

    ok, mensaje_error = usuario_service.cambiar_rol(g.usuario, id, nuevo_rol)

    if not ok:
        abort(400, description=mensaje_error)

    return jsonify(responses.success_response(mensaje="Rol actualizado")), 200

@main.route("/auditoria", methods=["GET"])
@login_required
@roles_required("admin")
def ver_auditoria():
    params = request.args.to_dict()

    filtros, orden, limit, page, offset, error = validators.validar_auditoria(params)

    if error:
        abort(400, description=error)

    logs = auditoria_service.obtener_auditoria(filtros, orden, limit, offset)

    return jsonify(responses.success_response(data=logs, meta={"page": page, "limit": limit})), 200