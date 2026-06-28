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

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = os.environ.get(
            "CORS_ALLOW_ORIGIN",
            "*",
        )
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    return app
