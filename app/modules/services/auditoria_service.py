from app.modules.db.db import get_connection

def registrar_accion(actor_id, accion, objetivo_id=None, entidad=None, descripcion=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO auditoria (actor_id, accion, objetivo_id, entidad, descripcion) VALUES (?, ?, ?, ?, ?)
        """, (actor_id, accion, objetivo_id, entidad, descripcion))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def obtener_auditoria(filtros, orden, limit, offset):
    try:
        conn = get_connection()
        cursor = conn.cursor()
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

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]
    finally:
        cursor.close()
        conn.close()