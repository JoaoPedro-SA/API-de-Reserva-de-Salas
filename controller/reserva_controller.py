from flask import Blueprint, request, jsonify
from model.bancoSQLite import BancoSQLite
import requests
from config import GESTAO_API_BASE_URL

reserva_bp = Blueprint('reserva_bp', __name__)

API_ESCOLAR_URL = f"{GESTAO_API_BASE_URL}/api/turma"

def validar_turma(turma_id):
    try:
        resposta = requests.get(f"{API_ESCOLAR_URL}/{turma_id}", timeout=10)
        return resposta.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Erro ao validar turma: {e}")
        return None

@reserva_bp.route('/reservas', methods=['POST'])
def criar_reserva():
    data = request.get_json(silent=True) or {}
    campos_obrigatorios = ["turma_id", "sala", "data", "hora_inicio", "hora_fim"]

    if not all(campo in data for campo in campos_obrigatorios):
        return jsonify({"erro": "Dados incompletos"}), 400

    turma_valida = validar_turma(data["turma_id"])
    if turma_valida is None:
        return jsonify({"erro": "Erro ao conectar com a API de turma"}), 503
    if not turma_valida:
        return jsonify({"erro": "Turma não encontrada"}), 404

    banco = BancoSQLite()
    try:
        banco.cursor.execute('''
            INSERT INTO Reservas (turma_id, sala, data, hora_inicio, hora_fim)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data["turma_id"],
            data["sala"],
            data["data"],
            data["hora_inicio"],
            data["hora_fim"]
        ))
        banco.conexao.commit()
        return jsonify({"mensagem": "Reserva criada com sucesso"}), 201
    except Exception as e:
        print("Erro ao inserir reserva:", e)
        return jsonify({"erro": "Erro ao criar reserva: " + str(e)}), 500
    finally:
        banco.close()

@reserva_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    banco = BancoSQLite()
    try:
        banco.cursor.execute("SELECT * FROM Reservas")
        linhas = banco.cursor.fetchall()
        reservas = [{
            "id": linha["id"],
            "turma_id": linha["turma_id"],
            "sala": linha["sala"],
            "data": linha["data"],
            "hora_inicio": linha["hora_inicio"],
            "hora_fim": linha["hora_fim"]
        } for linha in linhas]
        return jsonify(reservas)
    except Exception as e:
        print("Erro ao listar reservas:", e)
        return jsonify({"erro": "Erro ao buscar reservas"}), 500
    finally:
        banco.close()


@reserva_bp.route('/reservas/<int:reserva_id>', methods=['DELETE'])
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
