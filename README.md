# User Registration & Authentication API

A modular backend API built with **Python, Flask, SQLAlchemy, and SQLite**, focused on user registration, session-based authentication, role-based authorization, and audit logging.

The project was developed as a backend learning project with an emphasis on **separation of responsibilities, database interaction, authentication, authorization, validation, and testable business logic**.

---

## 🚀 Features

### 👤 User Management

* User registration
* Unique usernames
* Secure password hashing
* User login and logout
* Authenticated user profile
* Role management
* Protection against modifying your own role
* Default `user` role for newly registered accounts

### 🔐 Authentication & Authorization

* Session-based authentication using Flask sessions
* Password hashing and verification with Werkzeug
* Authentication decorator for protected endpoints
* Role-based authorization decorator
* Separate permissions for `user` and `admin` roles

### 📋 Audit Logging

The API maintains an audit trail for relevant actions performed by authenticated users.

Audit records include:

* Actor ID
* Action
* Target entity
* Target ID
* Description
* Timestamp

The audit endpoint also supports:

* Filtering by actor
* Filtering by action
* Filtering by entity
* Configurable ordering
* Pagination using `LIMIT` / `OFFSET` semantics

### 🧪 Testing

The project includes automated tests covering user and audit functionality using `pytest`.

Tests are organized separately from the application code:

```text
tests/
├── conftest.py
├── test_usuarios.py
└── test_auditoria.py
```

---

## 🛠️ Tech Stack

| Technology            | Purpose                           |
| --------------------- | --------------------------------- |
| **Python**            | Programming language              |
| **Flask**             | Web framework and HTTP API        |
| **SQLAlchemy**        | ORM and database interaction      |
| **SQLite**            | Relational database               |
| **Werkzeug Security** | Password hashing and verification |
| **python-dotenv**     | Environment variable management   |
| **pytest**            | Automated testing                 |

The current implementation uses **SQLAlchemy models and sessions** rather than relying exclusively on raw SQLite queries.

---

## 🏗️ Architecture

The project follows a modular, layered structure designed to keep HTTP handling, validation, business logic, and persistence separated.

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

### Request Flow

A typical request follows this flow:

```text
HTTP Request
     │
     ▼
  Authentication / Authorization
     │
     │   Decorators
     ▼
   Route
     │
     ▼
  Validator
     │
     ▼
  Service Layer
     │
     ▼
 SQLAlchemy Session
     │
     ▼
 Database
```

Decorators execute before the route function runs and act as access filters.

For example:

```python
@login_required
@roles_required("admin")
def cambiar_rol():
    ...
```

First, it is checked whether the user is authenticated, and subsequently, whether they possess the necessary role.

### Routes

`routes.py` is responsible for:

* Receiving HTTP requests
* Reading request data
* Calling validators
* Applying authentication/authorization
* Calling the appropriate service
* Returning HTTP responses

### Validators

`validators.py` centralizes input validation before data reaches the service layer.

This prevents business logic from becoming tightly coupled to request parsing.

### Services

The service layer contains the application's business logic.

For example, `usuario_service.py` handles operations such as:

* Creating users
* Authenticating users
* Retrieving profiles
* Changing roles
* Enforcing business rules

The service layer interacts with SQLAlchemy models through database sessions.

### Database Layer

The database module is responsible for SQLAlchemy configuration and session management.

The application currently uses SQLite through a SQLAlchemy database URL:

```text
sqlite:///usuarios.db
```

The database models define the `usuarios` and `auditoria` entities.

### Helpers

The `helpers` package provides reusable functionality such as:

* Standardized API responses
* Error handling

This keeps response formatting and exception handling out of the business logic.

---

## 🗄️ Database

The project uses SQLite for local development.

### `usuarios`

Stores registered users.

| Column     | Description     |
| ---------- | --------------- |
| `id`       | Primary key     |
| `username` | Unique username |
| `password` | Hashed password |
| `rol`      | User role       |

New users receive the `user` role by default.

### `auditoria`

Stores relevant actions performed within the application.

| Column        | Description                   |
| ------------- | ----------------------------- |
| `id`          | Primary key                   |
| `actor_id`    | User who performed the action |
| `accion`      | Action performed              |
| `objetivo_id` | Target user/entity ID         |
| `entidad`     | Target entity                 |
| `descripcion` | Additional information        |
| `fecha`       | Timestamp                     |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/Lev-w/registro-usuarios-sqlite.git
cd registro-usuarios-sqlite
```

## 2. Create a virtual environment

Using a virtual environment is recommended to keep the project's dependencies isolated from your global Python installation.

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

After activation, your terminal should indicate that the virtual environment is active.

---

## 3. Install dependencies

With the virtual environment activated, install the project's dependencies:

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
```

The application loads this value through `python-dotenv` and uses it as Flask's session secret key.

For a real deployment, use a strong, randomly generated secret and never commit the `.env` file to version control.

---

## 5. Run the application

Start the development server:

```bash
python run.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

The current entry point initializes the database, creates the Flask application, and starts Flask in debug mode.

---

# 📡 API Endpoints

The following are the main endpoints currently implemented by the API.

## Register a User

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

A newly registered user receives the `user` role by default.

---

## Login

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

If authentication succeeds, the API creates a Flask session containing the authenticated user's identity.

---

## Get Current User Profile

```http
GET /perfil
```

**Authentication required.**

### Example response

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

## Logout

```http
POST /logout
```

**Authentication required.**

The current session is cleared and the logout action is recorded in the audit log.

---

## Change User Role

```http
PUT /usuarios/<id>/rol
```

**Authentication:** Required
**Role:** `admin`

### Request

```json
{
  "rol": "admin"
}
```

Only administrators can change user roles.

The application also prevents an administrator from changing their own role.

---

## Get Audit Logs

```http
GET /auditoria
```

**Authentication:** Required
**Role:** `admin`

### Pagination

```http
GET /auditoria?page=1&limit=10
```

### Available filters

```text
actor_id
accion
entidad
orden
```

Example:

```http
GET /auditoria?actor_id=1&accion=LOGOUT&page=1&limit=10
```

The endpoint returns audit records together with pagination metadata.

---

# 🔒 Security Considerations

The project implements several basic security practices:

* Passwords are never stored in plain text.
* Passwords are hashed using Werkzeug's password hashing utilities.
* Authentication is handled through server-side sessions.
* Protected routes use authentication decorators.
* Administrative routes require the `admin` role.
* User input is validated before reaching the service layer.
* Role changes are subject to business rules.
* Important actions are recorded in an audit trail.

Password creation and verification are handled through `generate_password_hash` and `check_password_hash`.

> This project is intended for learning and local development. Additional hardening would be required before using it in a production environment.

---

# 🧪 Running Tests

The project includes tests for users and audit functionality.

Run the test suite with:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

Tests are located under:

```text
tests/
├── conftest.py
├── test_usuarios.py
└── test_auditoria.py
```

---

# 🎯 Project Goals

This project was created to practice and reinforce backend development concepts, including:

* Flask application structure
* REST API design
* Layered architecture
* SQL and relational databases
* SQLAlchemy ORM
* Database sessions
* Authentication
* Authorization
* Role-based access control
* Password hashing
* Input validation
* Business rules
* Audit logging
* Pagination
* Automated testing
* Environment configuration

The main goal is not simply to implement CRUD operations, but to understand how different backend responsibilities can be separated into maintainable components.

---

# 🔮 Future Improvements

Possible next steps for the project include:

* Separation using Repository Pattern
* Greater application of Clean Architecture principles
* Interfaces and Dependency Inversion
* JWT-based authentication
* Refresh tokens
* PostgreSQL support
* Database migrations with Alembic
* More comprehensive automated tests
* Docker support
* Rate limiting
* API documentation with OpenAPI/Swagger
* Production configuration
* Deployment
* Improved error and response schemas
* More advanced relational models

These improvements are not part of the current implementation and represent potential future developments for the project as its complexity increases.

---

# 👨‍💻 Author

Developed by **Lev** as a backend development project focused on Python, Flask, SQLAlchemy, authentication, authorization, and relational database design.

---

## 📄 License

This project is licensed under the **MIT License**.