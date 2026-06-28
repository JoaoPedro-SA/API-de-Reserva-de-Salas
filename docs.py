from flask import Blueprint, jsonify, Response

docs_bp = Blueprint("docs", __name__)

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "API de Reserva de Salas",
        "version": "1.0.0",
        "description": "Microservico para cadastro e listagem de reservas de salas por turma.",
    },
    "servers": [
        {"url": "https://api-de-reserva-de-salas.onrender.com"},
        {"url": "http://localhost:5001"},
    ],
    "paths": {
        "/reservas": {
            "get": {
                "summary": "Lista reservas",
                "responses": {
                    "200": {
                        "description": "Lista de reservas",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Reserva"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "summary": "Cria uma reserva",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/NovaReserva"},
                            "example": {
                                "turma_id": 1,
                                "sala": "101",
                                "data": "2026-06-28",
                                "hora_inicio": "08:00",
                                "hora_fim": "10:00",
                            },
                        }
                    },
                },
                "responses": {
                    "201": {"description": "Reserva criada"},
                    "400": {"description": "Dados incompletos"},
                    "404": {"description": "Turma nao encontrada"},
                    "503": {"description": "Erro ao conectar com a API de turma"},
                },
            },
        }
    },
    "components": {
        "schemas": {
            "Reserva": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "turma_id": {"type": "integer", "example": 1},
                    "sala": {"type": "string", "example": "101"},
                    "data": {"type": "string", "example": "2026-06-28"},
                    "hora_inicio": {"type": "string", "example": "08:00"},
                    "hora_fim": {"type": "string", "example": "10:00"},
                },
            },
            "NovaReserva": {
                "type": "object",
                "required": ["turma_id", "sala", "data", "hora_inicio", "hora_fim"],
                "properties": {
                    "turma_id": {"type": "integer", "example": 1},
                    "sala": {"type": "string", "example": "101"},
                    "data": {"type": "string", "example": "2026-06-28"},
                    "hora_inicio": {"type": "string", "example": "08:00"},
                    "hora_fim": {"type": "string", "example": "10:00"},
                },
            },
        }
    },
}


@docs_bp.get("/swagger.json")
def swagger_json():
    return jsonify(OPENAPI_SPEC)


@docs_bp.get("/docs")
def swagger_ui():
    html = """
<!doctype html>
<html>
  <head>
    <title>API de Reserva de Salas - Docs</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.onload = () => {
        window.ui = SwaggerUIBundle({
          url: "/swagger.json",
          dom_id: "#swagger-ui"
        });
      };
    </script>
  </body>
</html>
"""
    return Response(html, mimetype="text/html")
