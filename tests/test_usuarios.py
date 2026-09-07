import app.modules.services.usuario_service as usuario_service
from app.modules.db.db import get_connection

#--------------------------------CREAR USUARIO------------------------------------------------------

def test_crear_usuario(client):
    datos_usuario = {
        "username": "Juan",
        "password": "perez123"
    }

    response = client.post("/usuarios", json=datos_usuario)

    assert response.status_code == 201
    assert response.json["mensaje"] == "Usuario agregado."

def test_crear_usuario_sin_nombre(client):
    datos_usuario = {
        "username": "",
        "password": "perez123"
    }

    response = client.post("/usuarios", json=datos_usuario)

    assert response.status_code == 400
    assert response.json["error"] == "El username es obligatorio"

def test_crear_usuario_sin_password(client):
    datos_usuario = {
        "username": "Juan",
        "password": ""
    }

    response = client.post("/usuarios", json=datos_usuario)

    assert response.status_code == 400
    assert response.json["error"] == "La password es obligatoria"

def test_crear_usuario_existente(client, usuario):
    response = client.post("/usuarios", json=usuario)

    assert response.status_code == 400
    assert response.json["error"] == "El usuario ya existe"

def test_crear_usuario_sin_json(client):
    response = client.post("/usuarios", json="")

    assert response.status_code == 400
    assert response.json["error"] == "Se requiere JSON"

def test_crear_usuario_json_invalido(client):
    response = client.post("/usuarios", json=["usuario", "password"])

    assert response.status_code == 400
    assert response.json["error"] == "JSON inválido"

def test_crear_usuario_username_solo_espacios(client):
    response = client.post("/usuarios", json={
        "username": "   ",
        "password": "perez123"
    })

    assert response.status_code == 400
    assert response.json["error"] == "El username es obligatorio"

def test_crear_usuario_password_solo_espacios(client):
    response = client.post("/usuarios", json={
        "username": "Juan",
        "password": "   "
    })

    assert response.status_code == 400
    assert response.json["error"] == "La password es obligatoria"

def test_crear_usuario_duplicado_por_normalizacion(client, usuario):
    response = client.post("/usuarios", json={
        "username": "  JUAN  ",
        "password": "otra_clave"
    })

    assert response.status_code == 400
    assert response.json["error"] == "El usuario ya existe"

#----------------------------------LOGIN-------------------------------------------------------------

def test_login_exitoso(client, usuario):
    response = client.post("/login", json=usuario)
    
    assert response.status_code == 200
    assert response.json["mensaje"] == f"Login completado. Bienvenido, {usuario['username']}."

def test_login_usuario_inexistente(client):
    response = client.post("/login", json={
        "username": "niki",
        "password": "polea"
    })
    assert response.status_code == 401
    assert response.json["error"] == "Credenciales inválidas"

def test_login_sin_nombre(client):
    response = client.post("/login", json={
        "username": "",
        "password": "polea"
    })
    assert response.status_code == 400
    assert response.json["error"] == "Rellene el campo de username"

def test_login_sin_password(client):
    response = client.post("/login", json={
        "username": "niki",
        "password": ""
    })
    assert response.status_code == 400
    assert response.json["error"] == "Rellene el campo de password"

def test_login_sin_json(client):
    response = client.post("/login", json="")
    assert response.status_code == 400
    assert response.json["error"] == "Se requiere JSON"

def test_login_json_invalido(client):
    response = client.post("/login", json=["usuario", "password"])
    assert response.status_code == 400
    assert response.json["error"] == "JSON inválido"

def test_login_password_incorrecta(client, usuario):
    response = client.post("/login", json={
        "username": usuario["username"],
        "password": "clave_incorrecta"
    })

    assert response.status_code == 401
    assert response.json["error"] == "Credenciales inválidas"

#------------------------VER PERFIL-----------------------------------------------------------

def test_ver_mi_perfil_exitoso(client, cliente_logueado):
    response = client.get("/perfil")

    assert response.status_code == 200
    assert response.json["ok"] is True
    assert response.json["data"]["id"] == cliente_logueado["user_id"]
    assert response.json["data"]["username"] == cliente_logueado["username"]
    assert response.json["data"]["rol"] == "user"

def test_ver_mi_perfil_no_logueado(client, usuario):
    response = client.get("/perfil")

    assert response.status_code == 401
    assert response.json["error"] == "No autenticado"

def test_ver_mi_perfil_usuario_eliminado(client, cliente_logueado):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM usuarios WHERE id = ?", (cliente_logueado["user_id"],))
        conn.commit()
    finally:
        conn.close()

    response = client.get("/perfil")

    assert response.status_code == 404
    assert response.json["error"] == "Usuario no encontrado"

#--------------------------LOGOUT-----------------------------------

def test_logout_exitoso(client, cliente_logueado):
    response = client.post("/logout")

    assert response.status_code == 200
    assert response.json["mensaje"] == "Sesion cerrada"

    confirmar = client.get("/perfil")

    assert confirmar.status_code == 401
    assert confirmar.json["error"] == "No autenticado"

def test_logout_sin_logear(client, usuario):
    response = client.post("/logout")

    assert response.status_code == 401
    assert response.json["error"] == "No autenticado"

#--------------------------------CAMBIAR ROL---------------------------------------------------------

def test_cambiar_rol_sin_autenticacion(client, usuario):
    response = client.put(f"/usuarios/{usuario['user_id']}/rol", json={"rol": "admin"})

    assert response.status_code == 401
    assert response.json["error"] == "No autenticado"

def test_cambiar_rol_sin_permiso(client, cliente_logueado, usuario):
    response = client.put(f"/usuarios/{usuario['user_id']}/rol", json={"rol": "admin"})

    assert response.status_code == 403
    assert response.json["error"] == "No autorizado"

def test_cambiar_rol_sin_json(client, admin_logueado, usuario):
    response = client.put(f"/usuarios/{usuario['user_id']}/rol", json="")

    assert response.status_code == 400
    assert response.json["error"] == "Se requiere JSON"

def test_cambiar_rol_json_invalido(client, admin_logueado, usuario):
    response = client.put(f"/usuarios/{usuario['user_id']}/rol", json=["admin"])

    assert response.status_code == 400
    assert response.json["error"] == "JSON inválido"

def test_cambiar_rol_inexistente(client, admin_logueado, usuario):
    response = client.put(f"/usuarios/{usuario['user_id']}/rol", json={"rol": "superadmin"})

    assert response.status_code == 400
    assert response.json["error"] == "Elige un rol existente."

def test_cambiar_rol_a_si_mismo(client, admin_logueado):
    response = client.put(
        f"/usuarios/{admin_logueado['user_id']}/rol",
        json={"rol": "user"}
    )

    assert response.status_code == 400
    assert response.json["error"] == "No puedes modificarte a ti mismo."

def test_cambiar_rol_usuario_no_encontrado(client, admin_logueado):
    response = client.put("/usuarios/9999/rol", json={"rol": "admin"})

    assert response.status_code == 400
    assert response.json["error"] == "Usuario no encontrado"

def test_cambiar_rol_ya_asignado(client, admin_logueado, usuario):
    response = client.put(f"/usuarios/{usuario['user_id']}/rol", json={"rol": "user"})

    assert response.status_code == 400
    assert response.json["error"] == "Este usuario ya tiene ese rol."

def test_cambiar_rol_exitoso(client, admin_logueado, usuario):
    response = client.put(f"/usuarios/{usuario['user_id']}/rol", json={"rol": "admin"})

    assert response.status_code == 200
    assert response.json["ok"] is True
    assert response.json["mensaje"] == "Rol actualizado"

    perfil_objetivo = usuario_service.obtener_usuario("juan")
    assert perfil_objetivo["rol"] == "admin"