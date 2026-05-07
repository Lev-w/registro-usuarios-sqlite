from functools import wraps
from flask import session, g, abort
import app.modules.db as db

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            abort(401, description="No autenticado")

        usuario = db.obtener_perfil(session["user_id"])

        if not usuario:
            session.clear()
            abort(404, description="Usuario no encontrado")

        g.usuario = usuario

        return f(*args, **kwargs)
    return wrapper


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if g.usuario["rol"] not in roles:
                abort(403, description="No autorizado")

            return f(*args, **kwargs)
        return wrapper
    return decorator