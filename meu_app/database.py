import sqlite3
import json

DB_NAME = "rotina.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            horario TEXT NOT NULL,
            icone TEXT NOT NULL,
            dias TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            data TEXT NOT NULL,
            atividade_id TEXT NOT NULL,
            concluida INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (data, atividade_id)
        )
    """)
    conn.commit()
    conn.close()

def obter_atividades():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, horario, icone, dias FROM atividades")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r["id"],
            "nome": r["nome"],
            "horario": r["horario"],
            "icone": r["icone"],
            "dias": json.loads(r["dias"])
        }
        for r in rows
    ]

def salvar_atividade(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO atividades (id, nome, horario, icone, dias)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            nome=excluded.nome,
            horario=excluded.horario,
            icone=excluded.icone,
            dias=excluded.dias
    """, (data["id"], data["nome"], data["horario"], data["icone"], json.dumps(data["dias"])))
    conn.commit()
    conn.close()

def deletar_atividade(atividade_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM atividades WHERE id = ?", (atividade_id,))
    cursor.execute("DELETE FROM historico WHERE atividade_id = ?", (atividade_id,))
    conn.commit()
    conn.close()

def obter_historico():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT data, atividade_id, concluida FROM historico WHERE concluida = 1")
    rows = cursor.fetchall()
    conn.close()
    
    hist = {}
    for r in rows:
        data = r["data"]
        aid = r["atividade_id"]
        if data not in hist:
            hist[data] = {}
        hist[data][aid] = True
    return hist

def alternar_historico(data, atividade_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    if status:
        cursor.execute("""
            INSERT INTO historico (data, atividade_id, concluida)
            VALUES (?, ?, 1)
            ON CONFLICT(data, atividade_id) DO UPDATE SET concluida = 1
        """, (data, atividade_id))
    else:
        cursor.execute("DELETE FROM historico WHERE data = ? AND atividade_id = ?", (data, atividade_id))
    conn.commit()
    conn.close()