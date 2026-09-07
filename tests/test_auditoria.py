from app.modules.services.auditoria_service import registrar_accion, obtener_auditoria

FILTROS_VACIOS = {"actor_id": None, "accion": None, "entidad": None}


def _cargar_dataset():
    registrar_accion(10, "LOGOUT", objetivo_id=1, entidad="usuario")
    registrar_accion(10, "CAMBIAR_ROL", objetivo_id=2, entidad="usuario", descripcion="user → admin")
    registrar_accion(20, "LOGOUT", objetivo_id=3, entidad="usuario")
    registrar_accion(10, "LOGIN", objetivo_id=4, entidad="sesion")
    registrar_accion(20, "CAMBIAR_ROL", objetivo_id=5, entidad="producto")


def _ids(logs):
    return [log["id"] for log in logs]


#--------------------------------AUTH / PERMISOS-----------------------------------------------------

def test_ver_auditoria_sin_autenticacion(client):
    response = client.get("/auditoria")

    assert response.status_code == 401
    assert response.json["error"] == "No autenticado"

def test_ver_auditoria_sin_permiso(client, cliente_logueado):
    response = client.get("/auditoria")

    assert response.status_code == 403
    assert response.json["error"] == "No autorizado"

def test_ver_auditoria_exitoso(client, admin_logueado, cliente_logueado):
    client.post("/logout")
    client.post("/login", json={
        "username": admin_logueado["username"],
        "password": admin_logueado["password"]
    })

    response = client.get("/auditoria")

    assert response.status_code == 200
    assert response.json["ok"] is True
    assert response.json["meta"]["page"] == 1
    assert response.json["meta"]["limit"] == 50
    assert isinstance(response.json["data"], list)
    assert any(log["accion"] == "LOGOUT" for log in response.json["data"])

#--------------------------------VALIDACION DE QUERY PARAMS------------------------------------------

def test_ver_auditoria_actor_id_invalido(client, admin_logueado):
    response = client.get("/auditoria?actor_id=abc")

    assert response.status_code == 400
    assert response.json["error"] == "actor_id debe ser un número."

def test_ver_auditoria_limit_invalido(client, admin_logueado):
    response = client.get("/auditoria?limit=diez")

    assert response.status_code == 400
    assert response.json["error"] == "limit debe ser un número."

def test_ver_auditoria_page_invalida(client, admin_logueado):
    response = client.get("/auditoria?page=0")

    assert response.status_code == 400
    assert response.json["error"] == "page debe ser un numero mayor a 1."

def test_ver_auditoria_accion_invalida(client, admin_logueado):
    response = client.get("/auditoria?accion=HACKEAR")

    assert response.status_code == 400
    assert response.json["error"] == "Accion invalida."

#--------------------------------QUERIES HTTP--------------------------------------------------------

def test_ver_auditoria_filtra_cambiar_rol(client, admin_logueado, usuario):
    client.put(f"/usuarios/{usuario['user_id']}/rol", json={"rol": "admin"})

    response = client.get("/auditoria?accion=CAMBIAR_ROL")

    assert response.status_code == 200
    assert len(response.json["data"]) == 1
    log = response.json["data"][0]
    assert log["accion"] == "CAMBIAR_ROL"
    assert log["actor_id"] == admin_logueado["user_id"]
    assert log["objetivo_id"] == usuario["user_id"]
    assert log["entidad"] == "usuario"

def test_ver_auditoria_filtra_por_actor_id(client, admin_logueado, database):
    _cargar_dataset()

    response = client.get("/auditoria?actor_id=10")

    assert response.status_code == 200
    assert len(response.json["data"]) == 3
    assert all(log["actor_id"] == 10 for log in response.json["data"])

def test_ver_auditoria_filtra_por_entidad(client, admin_logueado, database):
    _cargar_dataset()

    response = client.get("/auditoria?entidad=sesion")

    assert response.status_code == 200
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["entidad"] == "sesion"
    assert response.json["data"][0]["accion"] == "LOGIN"

def test_ver_auditoria_filtra_por_accion_logout(client, admin_logueado, database):
    _cargar_dataset()

    response = client.get("/auditoria?accion=LOGOUT")

    assert response.status_code == 200
    assert len(response.json["data"]) == 2
    assert all(log["accion"] == "LOGOUT" for log in response.json["data"])

def test_ver_auditoria_filtra_por_accion_login(client, admin_logueado, database):
    _cargar_dataset()

    response = client.get("/auditoria?accion=LOGIN")

    assert response.status_code == 200
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["accion"] == "LOGIN"

def test_ver_auditoria_filtros_combinados(client, admin_logueado, database):
    _cargar_dataset()

    response = client.get("/auditoria?actor_id=20&accion=CAMBIAR_ROL&entidad=producto")

    assert response.status_code == 200
    assert len(response.json["data"]) == 1
    log = response.json["data"][0]
    assert log["actor_id"] == 20
    assert log["accion"] == "CAMBIAR_ROL"
    assert log["entidad"] == "producto"

def test_ver_auditoria_sin_resultados(client, admin_logueado, database):
    _cargar_dataset()

    response = client.get("/auditoria?actor_id=999")

    assert response.status_code == 200
    assert response.json["data"] == []

def test_ver_auditoria_paginacion(client, admin_logueado, database):
    _cargar_dataset()

    pagina_1 = client.get("/auditoria?limit=2&page=1")
    pagina_2 = client.get("/auditoria?limit=2&page=2")
    pagina_3 = client.get("/auditoria?limit=2&page=3")

    assert pagina_1.status_code == 200
    assert pagina_1.json["meta"] == {"page": 1, "limit": 2}
    assert _ids(pagina_1.json["data"]) == [5, 4]

    assert pagina_2.json["meta"] == {"page": 2, "limit": 2}
    assert _ids(pagina_2.json["data"]) == [3, 2]

    assert pagina_3.json["meta"] == {"page": 3, "limit": 2}
    assert _ids(pagina_3.json["data"]) == [1]

def test_ver_auditoria_orden_objetivo_id(client, admin_logueado, database):
    _cargar_dataset()

    response = client.get("/auditoria?orden=objetivo_id")

    assert response.status_code == 200
    assert [log["objetivo_id"] for log in response.json["data"]] == [5, 4, 3, 2, 1]

def test_ver_auditoria_orden_invalido_usa_id(client, admin_logueado, database):
    _cargar_dataset()

    response = client.get("/auditoria?orden=password")

    assert response.status_code == 200
    assert _ids(response.json["data"]) == [5, 4, 3, 2, 1]

#--------------------------------QUERIES SERVICIO----------------------------------------------------

def test_obtener_auditoria_sin_filtros_ordena_por_id_desc(database):
    _cargar_dataset()

    logs = obtener_auditoria(FILTROS_VACIOS, "id", 50, 0)

    assert len(logs) == 5
    assert _ids(logs) == [5, 4, 3, 2, 1]

def test_obtener_auditoria_dict_vacio_no_filtra(database):
    _cargar_dataset()

    logs = obtener_auditoria({}, "id", 50, 0)

    assert len(logs) == 5

def test_obtener_auditoria_filtra_actor_id(database):
    _cargar_dataset()

    logs = obtener_auditoria({"actor_id": 10, "accion": None, "entidad": None}, "id", 50, 0)

    assert len(logs) == 3
    assert all(log["actor_id"] == 10 for log in logs)

def test_obtener_auditoria_filtra_accion(database):
    _cargar_dataset()

    logs = obtener_auditoria({"accion": "CAMBIAR_ROL"}, "id", 50, 0)

    assert len(logs) == 2
    assert {log["actor_id"] for log in logs} == {10, 20}

def test_obtener_auditoria_filtra_entidad(database):
    _cargar_dataset()

    logs = obtener_auditoria({"entidad": "usuario"}, "id", 50, 0)

    assert len(logs) == 3
    assert all(log["entidad"] == "usuario" for log in logs)

def test_obtener_auditoria_actor_y_accion(database):
    _cargar_dataset()

    logs = obtener_auditoria({"actor_id": 10, "accion": "LOGOUT", "entidad": None}, "id", 50, 0)

    assert len(logs) == 1
    assert logs[0]["actor_id"] == 10
    assert logs[0]["accion"] == "LOGOUT"

def test_obtener_auditoria_actor_y_entidad(database):
    _cargar_dataset()

    logs = obtener_auditoria({"actor_id": 10, "entidad": "usuario"}, "id", 50, 0)

    assert len(logs) == 2
    assert all(log["actor_id"] == 10 and log["entidad"] == "usuario" for log in logs)

def test_obtener_auditoria_accion_y_entidad(database):
    _cargar_dataset()

    logs = obtener_auditoria({"accion": "CAMBIAR_ROL", "entidad": "producto"}, "id", 50, 0)

    assert len(logs) == 1
    assert logs[0]["objetivo_id"] == 5

def test_obtener_auditoria_tres_filtros(database):
    _cargar_dataset()

    logs = obtener_auditoria(
        {"actor_id": 20, "accion": "CAMBIAR_ROL", "entidad": "producto"},
        "id",
        50,
        0,
    )

    assert len(logs) == 1
    assert logs[0]["actor_id"] == 20

def test_obtener_auditoria_tres_filtros_sin_match(database):
    _cargar_dataset()

    logs = obtener_auditoria(
        {"actor_id": 10, "accion": "LOGIN", "entidad": "usuario"},
        "id",
        50,
        0,
    )

    assert logs == []

def test_obtener_auditoria_orden_objetivo_id_desc(database):
    _cargar_dataset()

    logs = obtener_auditoria(FILTROS_VACIOS, "objetivo_id", 50, 0)

    assert [log["objetivo_id"] for log in logs] == [5, 4, 3, 2, 1]

def test_obtener_auditoria_orden_actor_id_desc(database):
    _cargar_dataset()

    logs = obtener_auditoria(FILTROS_VACIOS, "actor_id", 50, 0)

    assert [log["actor_id"] for log in logs] == [20, 20, 10, 10, 10]

def test_obtener_auditoria_orden_fecha(database):
    _cargar_dataset()

    logs = obtener_auditoria(FILTROS_VACIOS, "fecha", 50, 0)

    assert len(logs) == 5
    assert all("fecha" in log for log in logs)

def test_obtener_auditoria_orden_invalido_cae_a_id(database):
    _cargar_dataset()

    logs = obtener_auditoria(FILTROS_VACIOS, "descripcion", 50, 0)

    assert _ids(logs) == [5, 4, 3, 2, 1]

def test_obtener_auditoria_orden_none_cae_a_id(database):
    _cargar_dataset()

    logs = obtener_auditoria(FILTROS_VACIOS, None, 50, 0)

    assert _ids(logs) == [5, 4, 3, 2, 1]

def test_obtener_auditoria_limit_y_offset(database):
    _cargar_dataset()

    primera = obtener_auditoria(FILTROS_VACIOS, "id", 2, 0)
    segunda = obtener_auditoria(FILTROS_VACIOS, "id", 2, 2)
    tercera = obtener_auditoria(FILTROS_VACIOS, "id", 2, 4)
    vacia = obtener_auditoria(FILTROS_VACIOS, "id", 2, 6)

    assert _ids(primera) == [5, 4]
    assert _ids(segunda) == [3, 2]
    assert _ids(tercera) == [1]
    assert vacia == []

def test_obtener_auditoria_limit_cero(database):
    _cargar_dataset()

    logs = obtener_auditoria(FILTROS_VACIOS, "id", 0, 0)

    assert logs == []
