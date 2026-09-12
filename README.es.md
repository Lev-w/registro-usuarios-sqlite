# API de Registro y Autenticación de Usuarios

API backend modular desarrollada con **Python, Flask, SQLAlchemy y SQLite**, enfocada en el registro de usuarios, autenticación mediante sesiones, autorización basada en roles y registro de auditoría.

El proyecto fue desarrollado como parte de un proceso de aprendizaje de backend, poniendo especial énfasis en la **separación de responsabilidades, interacción con bases de datos, autenticación, autorización, validación y lógica de negocio testeable**.

---

## 🚀 Características

### 👤 Gestión de usuarios

* Registro de usuarios
* Nombres de usuario únicos
* Hashing seguro de contraseñas
* Inicio y cierre de sesión
* Consulta del perfil del usuario autenticado
* Gestión de roles
* Protección contra la modificación del propio rol
* Asignación automática del rol `user` a los nuevos usuarios

### 🔐 Autenticación y autorización

* Autenticación mediante sesiones de Flask
* Hashing y verificación de contraseñas mediante Werkzeug
* Decorador para proteger endpoints que requieren autenticación
* Decorador para autorización basada en roles
* Permisos diferenciados para los roles `user` y `admin`

### 📋 Registro de auditoría

La API mantiene un registro de las acciones relevantes realizadas por los usuarios autenticados.

Los registros de auditoría incluyen:

* ID del actor
* Acción realizada
* Entidad objetivo
* ID del objetivo
* Descripción
* Fecha y hora

El endpoint de auditoría también permite:

* Filtrar por actor
* Filtrar por acción
* Filtrar por entidad
* Configurar el orden de los resultados
* Paginación mediante `LIMIT` / `OFFSET`

### 🧪 Tests

El proyecto incluye tests automatizados para las funcionalidades de usuarios y auditoría utilizando **pytest**.

Los tests están separados del código de aplicación:

```text
tests/
├── conftest.py
├── test_usuarios.py
└── test_auditoria.py
```

---

## 🛠️ Tecnologías utilizadas

| Tecnología            | Propósito                              |
| --------------------- | -------------------------------------- |
| **Python**            | Lenguaje de programación               |
| **Flask**             | Framework web y API HTTP               |
| **SQLAlchemy**        | ORM e interacción con la base de datos |
| **SQLite**            | Base de datos relacional               |
| **Werkzeug Security** | Hashing y verificación de contraseñas  |
| **python-dotenv**     | Gestión de variables de entorno        |
| **pytest**            | Tests automatizados                    |

La implementación actual utiliza **modelos y sesiones de SQLAlchemy ORM** para interactuar con la base de datos.

---

## 🏗️ Arquitectura

El proyecto utiliza una estructura modular y por capas, buscando mantener separadas las responsabilidades relacionadas con HTTP, validación, lógica de negocio y persistencia.

```text
registro-usuarios-sqlite/
│
├── app/
│   ├── helpers/
│   │   ├── errors.py
│   │   └── responses.py
│   │
│   ├── modules/
│   │   ├── db/
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   └── schema.sql
│   │   │
│   │   ├── services/
│   │   │   ├── auditoria_service.py
│   │   │   └── usuario_service.py
│   │   │
│   │   ├── decorators.py
│   │   ├── routes.py
│   │   └── validators.py
│   │
│   ├── config.py
│   └── __init__.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auditoria.py
│   └── test_usuarios.py
│
├── run.py
├── requirements.txt
├── .env
└── README.md
```

### Flujo de una petición

Una petición típica sigue aproximadamente este flujo:

```text
HTTP Request
     │
     ▼
Autenticación / Autorización
     │
     │  Decoradores
     ▼
   Route
     │
     ▼
  Validator
     │
     ▼
Application Service
     │
     ▼
  SQLAlchemy
     │
     ▼
  Database
```

Los decoradores se ejecutan antes de que la función de la ruta sea ejecutada y funcionan como filtros de acceso.

Por ejemplo:

```python
@login_required
@roles_required("admin")
def cambiar_rol():
    ...
```

Primero se comprueba si el usuario está autenticado y posteriormente si posee el rol necesario.

### Routes

`routes.py` es responsable de manejar la capa HTTP.

Entre sus responsabilidades se encuentran:

* Recibir peticiones HTTP
* Obtener los datos enviados por el cliente
* Aplicar validaciones
* Aplicar autenticación y autorización
* Llamar al service correspondiente
* Construir las respuestas HTTP

### Validators

`validators.py` centraliza la validación de los datos recibidos antes de que estos lleguen a la lógica de negocio.

Esto permite evitar que la validación de entradas quede mezclada con las reglas de negocio.

Por ejemplo, un validator puede comprobar que:

* Un campo obligatorio exista
* Un valor tenga el tipo esperado
* Un rol pertenezca a los valores permitidos
* Los datos tengan el formato esperado

### Services

La capa de services contiene la lógica de negocio de la aplicación.

Por ejemplo, `usuario_service.py` se encarga de operaciones como:

* Crear usuarios
* Autenticar usuarios
* Obtener perfiles
* Cambiar roles
* Aplicar reglas de negocio relacionadas con usuarios

Esta capa también interactúa con SQLAlchemy para realizar las operaciones de persistencia.

### Database

El módulo de base de datos es responsable de la configuración de SQLAlchemy y de la gestión de las sesiones.

Actualmente el proyecto utiliza SQLite mediante una URL de base de datos:

```text
sqlite:///usuarios.db
```

Los modelos de SQLAlchemy representan las entidades utilizadas por la aplicación.

### Helpers

El paquete `helpers` contiene funcionalidades reutilizables como:

* Respuestas estandarizadas
* Manejo de errores

Esto evita duplicar lógica relacionada con las respuestas y errores HTTP dentro de las rutas.

---

## 🗄️ Base de datos

El proyecto utiliza **SQLite** como base de datos para el desarrollo local.

### `usuarios`

Almacena los usuarios registrados.

| Columna    | Descripción                            |
| ---------- | -------------------------------------- |
| `id`       | Clave primaria                         |
| `username` | Nombre de usuario único                |
| `password` | Contraseña almacenada mediante hashing |
| `rol`      | Rol del usuario                        |

Los nuevos usuarios reciben el rol `user` por defecto.

### `auditoria`

Almacena las acciones relevantes realizadas dentro de la aplicación.

| Columna       | Descripción                       |
| ------------- | --------------------------------- |
| `id`          | Clave primaria                    |
| `actor_id`    | Usuario que realizó la acción     |
| `accion`      | Acción realizada                  |
| `objetivo_id` | ID del usuario o entidad objetivo |
| `entidad`     | Entidad afectada                  |
| `descripcion` | Información adicional             |
| `fecha`       | Fecha y hora de la acción         |

---

# ⚙️ Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/Lev-w/registro-usuarios-sqlite.git
cd registro-usuarios-sqlite
```

## 2. Crear un entorno virtual

Se recomienda utilizar un entorno virtual para mantener las dependencias del proyecto aisladas de la instalación global de Python.

### Windows

```bash
python -m venv venv
```

Activar el entorno virtual:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activar el entorno virtual:

```bash
source venv/bin/activate
```

---

## 3. Instalar las dependencias

Con el entorno virtual activado, instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

---

## 4. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=your-secret-key
```

La aplicación utiliza esta variable como clave secreta de Flask para la gestión de sesiones.

Para un entorno real, se recomienda utilizar una clave segura y generada aleatoriamente, además de evitar subir el archivo `.env` al repositorio.

---

## 5. Ejecutar la aplicación

Inicia el servidor de desarrollo:

```bash
python run.py
```

La aplicación estará disponible en:

```text
http://127.0.0.1:5000
```

---

# 📡 Endpoints de la API

A continuación se muestran algunos de los principales endpoints implementados por la API.

## Registrar un usuario

```http
POST /usuarios
```

### Request

```json
{
  "username": "martin",
  "password": "strong-password"
}
```

### Response

```json
{
  "ok": true,
  "mensaje": "Usuario agregado."
}
```

Los nuevos usuarios reciben automáticamente el rol `user`.

---

## Iniciar sesión

```http
POST /login
```

### Request

```json
{
  "username": "martin",
  "password": "strong-password"
}
```

Si las credenciales son válidas, la aplicación crea una sesión de Flask para el usuario autenticado.

---

## Obtener perfil

```http
GET /perfil
```

**Requiere autenticación.**

### Ejemplo de respuesta

```json
{
  "ok": true,
  "data": {
    "id": 1,
    "username": "martin",
    "rol": "user"
  },
  "mensaje": "Perfil obtenido"
}
```

---

## Cerrar sesión

```http
POST /logout
```

**Requiere autenticación.**

La sesión actual es eliminada y la acción de logout queda registrada en el sistema de auditoría.

---

## Cambiar rol de un usuario

```http
PUT /usuarios/<id>/rol
```

**Autenticación:** Requerida
**Rol:** `admin`

### Request

```json
{
  "rol": "admin"
}
```

Solo los administradores pueden modificar los roles de los usuarios.

Además, el sistema evita que un administrador modifique su propio rol.

---

## Obtener registros de auditoría

```http
GET /auditoria
```

**Autenticación:** Requerida
**Rol:** `admin`

### Paginación

```http
GET /auditoria?page=1&limit=10
```

### Filtros disponibles

```text
actor_id
accion
entidad
orden
```

Ejemplo:

```http
GET /auditoria?actor_id=1&accion=LOGOUT&page=1&limit=10
```

El endpoint devuelve los registros junto con información relacionada con la paginación.

---

# 🔒 Consideraciones de seguridad

El proyecto implementa varias prácticas básicas de seguridad:

* Las contraseñas no se almacenan en texto plano.
* Las contraseñas utilizan hashing mediante Werkzeug.
* La autenticación utiliza sesiones del servidor.
* Las rutas protegidas utilizan decoradores de autenticación.
* Las rutas administrativas requieren el rol `admin`.
* Los datos de entrada son validados antes de llegar a la lógica de negocio.
* Los cambios de rol están sujetos a reglas de negocio.
* Las acciones relevantes quedan registradas en una auditoría.

La creación y verificación de contraseñas se realiza utilizando las herramientas de hashing proporcionadas por Werkzeug.

> Este proyecto está orientado al aprendizaje y al desarrollo local. Serían necesarias medidas adicionales antes de utilizarlo en un entorno de producción.

---

# 🧪 Ejecutar los tests

El proyecto incluye tests automatizados para las funcionalidades de usuarios y auditoría.

Ejecutar todos los tests:

```bash
pytest
```

Para obtener información más detallada:

```bash
pytest -v
```

Los tests se encuentran en:

```text
tests/
├── conftest.py
├── test_usuarios.py
└── test_auditoria.py
```

---

# 🎯 Objetivos del proyecto

Este proyecto fue desarrollado para practicar y reforzar conceptos de backend, incluyendo:

* Estructuración de aplicaciones Flask
* Diseño de APIs REST
* Arquitectura por capas
* Bases de datos relacionales
* SQLAlchemy ORM
* Gestión de sesiones de base de datos
* Autenticación
* Autorización
* Control de acceso basado en roles
* Hashing de contraseñas
* Validación de datos
* Reglas de negocio
* Registro de auditoría
* Paginación
* Tests automatizados
* Configuración mediante variables de entorno

El objetivo principal no es simplemente implementar operaciones CRUD, sino comprender cómo separar las distintas responsabilidades de una aplicación backend para obtener un código más mantenible y fácil de probar.

---

# 🔮 Futuras mejoras

Algunas mejoras que podrían incorporarse posteriormente:

* Separación mediante Repository Pattern
* Mayor aplicación de principios de Clean Architecture
* Interfaces y Dependency Inversion
* Autenticación mediante JWT
* Refresh tokens
* Soporte para PostgreSQL
* Migraciones de base de datos mediante Alembic
* Mayor cobertura de tests automatizados
* Docker
* Rate limiting
* Documentación de la API mediante OpenAPI/Swagger
* Configuración específica para producción
* Deployment
* Mejora de los esquemas de respuestas y errores
* Modelos relacionales adicionales

Estas mejoras no forman parte de la implementación actual y representan posibles evoluciones del proyecto a medida que aumente su complejidad.

---

# 👨‍💻 Autor

Desarrollado por **Lev** como proyecto de aprendizaje y desarrollo backend, enfocado en Python, Flask, SQLAlchemy, autenticación, autorización y diseño de bases de datos relacionales.

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.
