import os
import sqlite3

# Define o caminho do banco no mesmo diretório do app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "exames_sst.db")

# Conecta usando o caminho correto
conn = sqlite3.connect(DB_PATH)