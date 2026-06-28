from flask import Blueprint, request, jsonify
from model.bancoSQLite import BancoSQLite
import requests
from config import GESTAO_API_BASE_URL

routes = Blueprint("routes", __name__)


def validar_turma(turma_id):
    try:
        resp = requests.get(f"{GESTAO_API_BASE_URL}/api/turma/{turma_id}", timeout=10)
        return resp.status_code == 200
    except requests.RequestException:
        return False

@routes.route("/reservas", methods=["POST"])
def criar_reserva():
    dados = request.get_json(silent=True) or {}
    turma_id = dados.get("turma_id")

    if not validar_turma(turma_id):
        return jsonify({"erro": "Turma não encontrada"}), 400

    banco = BancoSQLite()
    try:
        banco.cursor.execute(
            "INSERT INTO Reservas (turma_id, sala, data, hora_inicio, hora_fim) VALUES (?, ?, ?, ?, ?)",
            (turma_id, dados.get("sala"), dados.get("data"), dados.get("hora_inicio"), dados.get("hora_fim")),
        )
        banco.conexao.commit()
    finally:
        banco.close()

    return jsonify({"mensagem": "Reserva criada com sucesso"}), 201

@routes.route("/reservas", methods=["GET"])
def listar_reservas():
    banco = BancoSQLite()
    try:
        banco.cursor.execute("SELECT * FROM Reservas")
        reservas = banco.cursor.fetchall()
        return jsonify([
            {
                "id": r["id"],
                "turma_id": r["turma_id"],
                "sala": r["sala"],
                "data": r["data"],
                "hora_inicio": r["hora_inicio"],
                "hora_fim": r["hora_fim"]
            } for r in reservas
        ])
    finally:
        banco.close()
