import sqlite3
from pathlib import Path
import app.config as config

BASE_DIR = Path(__file__).parent
schema_path = BASE_DIR / 'schema.sql'

def get_connection():
    print(f"\n[CONEXIÓN DB] Conectando a: {config.DATABASE_NAME}")
    con = sqlite3.connect(config.DATABASE_NAME)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys = ON')
    return con

def init_db():
    con = get_connection()
    with open(schema_path, encoding="utf-8") as archivo:
        sql = archivo.read()
    con.executescript(sql)
    con.commit()
    con.close()