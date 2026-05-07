def validar_usuario(data):
    if not data:
        return None, "Se requiere JSON"
    
    username = data.get("username")
    password = data.get("password")

    if not username or not username.strip():
        return None, "El username es obligatorio"
    
    if not password or not password.strip():
        return None, "La password es obligatoria"
    
    username = username.strip().lower()
    password = password.strip()

    datos_limpios = {
        "username": username,
        "password": password
    }

    return datos_limpios, None

def validar_login(data):
    if not data:
        return None, "Se requiere JSON"
    
    username = data.get("username")
    password = data.get("password")

    if not username or not username.strip():
        return None, "Rellene el campo de username"
    
    if not password or not password.strip():
        return None, "Rellene el campo de password"
    
    username = username.strip().lower()

    datos_limpios = {
        "username": username,
        "password": password
        }

    return datos_limpios, None

def validar_cambio_rol(data):
    if not data:
        return None, "Se requiere JSON"

    if not isinstance(data, dict):
        return None, "JSON inválido"

    nuevo_rol = data.get("rol")

    roles_validos = ["user", "admin"]

    if not nuevo_rol or nuevo_rol not in roles_validos:
        return None, "Elige un rol existente."
    
    return nuevo_rol, None

def validar_auditoria(data):
    if not data:
        data = {}

    acciones_validas = {"LOGIN", "LOGOUT", "CAMBIAR_ROL"}

    actor_id = data.get("actor_id")
    accion = data.get("accion")
    entidad = data.get("entidad")
    orden = data.get("orden")
    limit = data.get("limit", 50)
    page = data.get("page", 1)

    if actor_id is not None:
        try:
            actor_id = int(actor_id)
        except ValueError:
            return None, None, None, None, None, "actor_id debe ser un número."

    if limit is not None:    
        try:
            limit = int(limit)
        except ValueError:
            return None, None, None, None, None, "limit debe ser un número."
        
    if page is not None:
        try:
            page = int(page)
            if page < 1:
                raise ValueError
        except ValueError:
            return None, None, None, None, None, "page debe ser un numero mayor a 1."
        
    offset = (page - 1) * limit
        
    filtros = {
        "actor_id": actor_id,
        "accion": accion,
        "entidad": entidad
    }

    if accion and accion not in acciones_validas:
        return None, None, None, None, None, "Accion invalida."
    
    return filtros, orden, limit, page, offset, None