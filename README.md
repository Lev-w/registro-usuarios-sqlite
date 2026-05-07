# Sistema de Registro de Usuarios API

API backend desarrollada con Flask y SQLite enfocada en autenticación, manejo de sesiones, roles, auditoría y arquitectura backend modular.

## 🚀 Tecnologías utilizadas

* Python
* Flask
* SQLite
* Werkzeug Security
* python-dotenv

---

# 📚 Características

## Usuarios

* Registro de usuarios
* Login con sesión persistente
* Logout
* Perfil de usuario

## Seguridad

* Hash de contraseñas
* Validaciones de entrada
* Manejo de sesiones
* Decorators de autenticación y autorización

## Roles

* Sistema de roles (`user`, `admin`)
* Protección de rutas por rol
* Cambio de roles por administrador

## Auditoría

* Registro de acciones importantes
* Filtros dinámicos
* Paginación (`LIMIT + OFFSET`)
* Ordenamiento configurable

## Arquitectura

Proyecto dividido por responsabilidades:

```text
app/
    helpers/
        errors.py
        responses.py
    modules/
        db.py
        routes.py
        validators.py
        decorators.py
        services/
            auditoria_service.py
            usuario_service.py
    init.py
run.py
```

---

# ⚙️ Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/Lev-w/registro-usuarios-sqlite
cd registro-usuarios-sqlite
```

---

## 2. Crear entorno virtual

```bash
python -m venv venv
```

### Activar entorno virtual

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Crear archivo `.env`

```env
SECRET_KEY=tu_clave_secreta
```

---

## 5. Ejecutar proyecto

```bash
python run.py
```

---

# 📌 Endpoints principales

## Crear usuario

```http
POST /usuarios
```

Body:

```json
{
  "username": "martin",
  "password": "1234"
}
```

---

## Login

```http
POST /login
```

---

## Perfil

```http
GET /perfil
```

---

## Logout

```http
POST /logout
```

---

## Cambiar rol

```http
PUT /usuarios/<id>/rol
```

---

## Auditoría

```http
GET /auditoria?page=1&limit=10
```

Filtros disponibles:

* actor_id
* accion
* entidad
* orden

---

# 🧠 Objetivo del proyecto

Este proyecto fue desarrollado como práctica para aprender:

* Arquitectura backend
* Flask
* SQL y SQLite
* Autenticación
* Roles y permisos
* Diseño de APIs
* Validaciones
* Auditoría
* Paginación

---

# 🔮 Mejoras futuras

* JWT Authentication
* PostgreSQL
* Relaciones SQL avanzadas
* Tests automáticos
* Docker
* Refresh tokens
* Rate limiting
* Deploy

---

# 👨‍💻 Autor

Proyecto realizado por Lev como práctica de backend con Python y Flask.