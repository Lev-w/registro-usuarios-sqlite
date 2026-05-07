import sqlite3
from werkzeug.security import check_password_hash

DB_NAME = "usuarios.db"

def conectar():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    return con

#-------------------------------USUARIOS---------------------------

def crear_tabla():
    with conectar() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                rol TEXT DEFAULT 'user'
            )"""
        )

def crear_usuario(username, password):
    with conectar() as con:
        con.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            (username, password)
        )

def obtener_usuario(username):
    with conectar() as con:
        return con.execute(
            "SELECT * FROM usuarios WHERE username = ?",
            (username,)
        ).fetchone()
    
def login(username, password):
    usuario = obtener_usuario(username)

    if not usuario:
        return None

    if check_password_hash(usuario["password"], password):
        return usuario
    
    return None

def obtener_perfil(id):
    with conectar() as con:
        return con.execute(
            "SELECT * FROM usuarios WHERE id = ?", (id,)
        ).fetchone()

def actualizar_rol(id, rol):
    with conectar() as con:
        cursor = con.execute(
            "UPDATE usuarios SET rol = ? WHERE id = ?",
            (rol, id)
        )
        return cursor.rowcount

#-------------------------------AUDITORIA-------------------------------

def crear_tabla_auditoria():
    with conectar() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor_id INTEGER NOT NULL,
                accion TEXT NOT NULL,
                objetivo_id INTEGER,
                entidad TEXT,
                descripcion TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )

def registrar_accion(actor_id, accion, objetivo_id=None, entidad=None, descripcion=None):
    with conectar() as con:
        con.execute("""
            INSERT INTO auditoria (actor_id, accion, objetivo_id, entidad, descripcion) VALUES (?, ?, ?, ?, ?)
        """, (actor_id, accion, objetivo_id, entidad, descripcion))

def obtener_auditoria(filtros, orden, limit, offset):
    with conectar() as con:
        query = "SELECT * FROM auditoria WHERE 1=1"
        params = []

        columnas_validas = ["id", "objetivo_id", "fecha", "actor_id"]
        if orden not in columnas_validas:
            orden = "id"

        if filtros.get("actor_id") is not None:
            query += " AND actor_id = ?"
            params.append(filtros["actor_id"])

        if filtros.get("accion") is not None:
            query += " AND accion = ?"
            params.append(filtros["accion"])
    
        if filtros.get("entidad") is not None:
            query += " AND entidad = ?"
            params.append(filtros["entidad"])
        
        query += f" ORDER BY {orden} DESC LIMIT ? OFFSET ?"
        params.append(limit)
        params.append(offset)

        return con.execute(query, params).fetchall()