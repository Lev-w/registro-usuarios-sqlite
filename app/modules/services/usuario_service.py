import app.modules.db as db

def login(datos):
    usuario = db.login(**datos)

    if not usuario:
        return None

    db.registrar_accion(
        actor_id=usuario["id"],
        accion="LOGIN",
        entidad="usuario"
    )

    return usuario


def cambiar_rol(actor, objetivo_id, nuevo_rol):
    if actor["id"] == objetivo_id:
        return None, "No puedes modificarte a ti mismo."

    usuario_objetivo = db.obtener_perfil(objetivo_id)

    if not usuario_objetivo:
        return None, "Usuario no encontrado"

    if usuario_objetivo["rol"] == nuevo_rol:
        return None, "Este usuario ya tiene ese rol."

    actualizado = db.actualizar_rol(objetivo_id, nuevo_rol)

    if not actualizado:
        return None, "Usuario no encontrado"

    db.registrar_accion(
        actor_id=actor["id"],
        accion="CAMBIAR_ROL",
        objetivo_id=objetivo_id,
        entidad="usuario",
        descripcion=f"{usuario_objetivo['rol']} → {nuevo_rol}"
    )

    return True, None