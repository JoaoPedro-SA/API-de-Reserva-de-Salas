class Reserva:
    def __init__(self, turma_id, sala, data, hora_inicio, hora_fim, id=None):
        self.id = id
        self.turma_id = turma_id
        self.sala = sala
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
