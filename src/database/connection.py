import sqlite3
import os
from pathlib import Path

# Define o caminho para a raiz do projeto e o arquivo do banco SQLite
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "controle_exames.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn


def init_db():
    """Inicializa o banco de dados executando o arquivo schema.sql."""
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Arquivo de schema não encontrado em: {SCHEMA_PATH}")

    with get_connection() as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_script = f.read()
        conn.executescript(schema_script)
        conn.commit()
    print("✅ Banco de dados inicializado com sucesso!")


if __name__ == "__main__":
    init_db()