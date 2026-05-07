import app.modules.db as db

def obtener_logs(filtros, orden, limit, offset):
    return db.obtener_auditoria(filtros, orden, limit, offset)