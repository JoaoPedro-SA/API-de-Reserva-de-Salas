import os
import sqlite3

import requests

from config import GESTAO_API_BASE_URL
from config import banco_de_dados as bd


def _garantir_diretorio_banco():
    db_dir = os.path.dirname(os.path.abspath(bd))
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)


def importar_professores_da_api():
    url = f"{GESTAO_API_BASE_URL}/api/professores"

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        professores = resposta.json()

        conexao = sqlite3.connect(bd)
        cursor = conexao.cursor()
        for prof in professores:
            cursor.execute(
                "INSERT OR IGNORE INTO professores (id, nome, disciplina) VALUES (?, ?, ?)",
                (prof["id"], prof["nome"], prof["disciplina"]),
            )

        conexao.commit()
        conexao.close()
        print("Professores importados com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar professores da API: {e}")


def importar_turmas_da_api():
    url = f"{GESTAO_API_BASE_URL}/api/turma"

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        turmas = resposta.json()

        conexao = sqlite3.connect(bd)
        conexao.execute("PRAGMA foreign_keys = ON")
        cursor = conexao.cursor()
        for turma in turmas:
            cursor.execute(
                """
                INSERT OR IGNORE INTO turmas (id, nome, turno, professor_id, ativo)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    turma["id"],
                    turma["nome"],
                    turma["turno"],
                    turma["professor_id"],
                    turma["ativo"],
                ),
            )

        conexao.commit()
        conexao.close()
        print("Turmas importadas com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar API de turmas: {e}")


def inicializar_banco():
    _garantir_diretorio_banco()
    conexao = sqlite3.connect(bd)
    conexao.execute("PRAGMA foreign_keys = ON")
    cursor = conexao.cursor()
    print("Conexao com o banco de dados estabelecida.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            disciplina TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turno TEXT NOT NULL,
            professor_id INTEGER NOT NULL,
            ativo BOOLEAN NOT NULL,
            FOREIGN KEY (professor_id) REFERENCES professores (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turma_id INTEGER,
            sala TEXT,
            data TEXT,
            hora_inicio TEXT,
            hora_fim TEXT,
            FOREIGN KEY (turma_id) REFERENCES turmas(id)
        )
    """)

    conexao.commit()
    conexao.close()
    print("Banco de dados inicializado com sucesso!")


class BancoSQLite:
    def __init__(self):
        _garantir_diretorio_banco()
        self.conexao = sqlite3.connect(bd)
        self.conexao.execute("PRAGMA foreign_keys = ON")
        self.conexao.row_factory = sqlite3.Row
        self.cursor = self.conexao.cursor()

    def close(self):
        if self.conexao:
            self.conexao.close()

    def conectar_banco(self):
        return sqlite3.connect(bd)
