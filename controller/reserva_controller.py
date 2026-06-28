from flask import Blueprint, jsonify, request
import requests

from config import GESTAO_API_BASE_URL
from model.bancoSQLite import BancoSQLite

reserva_bp = Blueprint("reserva_bp", __name__)

API_ESCOLAR_URL = f"{GESTAO_API_BASE_URL}/api/turma"


def validar_turma(turma_id):
    try:
        resposta = requests.get(f"{API_ESCOLAR_URL}/{turma_id}", timeout=10)
        return resposta.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Erro ao validar turma: {e}")
        return None


@reserva_bp.route("/reservas", methods=["POST"])
def criar_reserva():
    data = request.get_json(silent=True) or {}
    campos = ["turma_id", "sala", "data", "hora_inicio", "hora_fim"]
    if not all(campo in data for campo in campos):
        return jsonify({"erro": "Dados incompletos"}), 400
    if not str(data["turma_id"]).isdigit():
        return jsonify({"erro": "turma_id deve ser um numero inteiro"}), 400
    if not str(data["sala"]).strip():
        return jsonify({"erro": "sala e obrigatoria"}), 400
    if str(data["hora_inicio"]) >= str(data["hora_fim"]):
        return jsonify({"erro": "hora_inicio deve ser menor que hora_fim"}), 400

    turma_id = int(data["turma_id"])
    turma_valida = validar_turma(turma_id)
    if turma_valida is None:
        return jsonify({"erro": "Erro ao conectar com a API de turma"}), 503
    if not turma_valida:
        return jsonify({"erro": "Turma nao encontrada"}), 404

    banco = BancoSQLite()
    try:
        banco.cursor.execute(
            """
            INSERT INTO Reservas (turma_id, sala, data, hora_inicio, hora_fim)
            VALUES (?, ?, ?, ?, ?)
            """,
            (turma_id, data["sala"], data["data"], data["hora_inicio"], data["hora_fim"]),
        )
        banco.conexao.commit()
        return jsonify({"mensagem": "Reserva criada com sucesso", "id": banco.cursor.lastrowid}), 201
    except Exception as e:
        print("Erro ao inserir reserva:", e)
        return jsonify({"erro": "Erro ao criar reserva: " + str(e)}), 500
    finally:
        banco.close()


@reserva_bp.route("/reservas", methods=["GET"])
def listar_reservas():
    banco = BancoSQLite()
    try:
        banco.cursor.execute("SELECT * FROM Reservas")
        linhas = banco.cursor.fetchall()
        return jsonify([
            {
                "id": linha["id"],
                "turma_id": linha["turma_id"],
                "sala": linha["sala"],
                "data": linha["data"],
                "hora_inicio": linha["hora_inicio"],
                "hora_fim": linha["hora_fim"],
            }
            for linha in linhas
        ])
    except Exception as e:
        print("Erro ao listar reservas:", e)
        return jsonify({"erro": "Erro ao buscar reservas"}), 500
    finally:
        banco.close()


@reserva_bp.route("/reservas/<int:reserva_id>", methods=["DELETE"])
def deletar_reserva(reserva_id):
    banco = BancoSQLite()
    try:
        banco.cursor.execute("DELETE FROM Reservas WHERE id = ?", (reserva_id,))
        banco.conexao.commit()
        if banco.cursor.rowcount == 0:
            return jsonify({"erro": "Reserva nao encontrada"}), 404
        return jsonify({"mensagem": "Reserva removida com sucesso"}), 200
    except Exception as e:
        print("Erro ao deletar reserva:", e)
        return jsonify({"erro": "Erro ao deletar reserva: " + str(e)}), 500
    finally:
        banco.close()
