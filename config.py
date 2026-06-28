import os
from flask import Flask
banco_de_dados = "banco_de_dados.db"
GESTAO_API_BASE_URL = os.environ.get(
    "GESTAO_API_BASE_URL",
    "https://api-de-gerenciamento-escolar.onrender.com"
).rstrip("/")

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    return app
