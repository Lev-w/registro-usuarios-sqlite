import pytest
from sqlalchemy import select
from app import create_app
import app.config as config
from app.modules.db.db import init_db, reset_db, get_session
from app.modules.db.models import UsuarioModel
import app.modules.services.usuario_service as usuario_service


@pytest.fixture
def database():
    config.DATABASE_URL = "sqlite:///:memory:"
    init_db(config.DATABASE_URL)

    yield

    reset_db()


@pytest.fixture
def client(database):
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def usuario(client):
    datos_usuario = {
        "username": "Juan",
        "password": "perez123"
    }

    response = client.post("/usuarios", json=datos_usuario)

    assert response.status_code == 201

    usuario_db = usuario_service.obtener_usuario("juan")

    return {
        "username": datos_usuario["username"],
        "password": datos_usuario["password"],
        "user_id": usuario_db["id"]
    }


@pytest.fixture
def cliente_logueado(client):
    datos_usuario = {
        "username": "martin_test",
        "password": "password123"
    }

    client.post("/usuarios", json=datos_usuario)

    usuario_db = usuario_service.obtener_usuario("martin_test")

    client.post("/login", json=datos_usuario)

    return {
        "username": usuario_db["username"],
        "password": datos_usuario["password"],
        "user_id": usuario_db["id"]
    }


@pytest.fixture
def admin_logueado(client):
    datos_usuario = {
        "username": "admin_test",
        "password": "adminpass123"
    }

    response = client.post("/usuarios", json=datos_usuario)
    assert response.status_code == 201

    session = get_session()
    try:
        admin = session.scalar(
            select(UsuarioModel).where(UsuarioModel.username == "admin_test")
        )
        admin.rol = "admin"
        session.commit()
    finally:
        session.close()

    usuario_db = usuario_service.obtener_usuario("admin_test")
    login = client.post("/login", json=datos_usuario)
    assert login.status_code == 200

    return {
        "username": usuario_db["username"],
        "password": datos_usuario["password"],
        "user_id": usuario_db["id"]
    }
