from app.database import db


class Turma(db.Model):
    """
    Representa um agendamento específico de um treinamento do catálogo.
    Esta classe será mapeada para a tabela 'turmas'.
    """

    __tablename__ = 'turmas'

    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(50), nullable=True)  # Ex: "09:00 - 18:00"
    # Ex: "Online" ou "Sala 3"
    local = db.Column(db.String(150), nullable=True)
    # Ex: Agendada, Em andamento, Concluída
    status = db.Column(db.String(50), nullable=False, default='Agendada')

    # --- Relações (Chaves Estrangeiras) ---

    # 1. Qual treinamento do catálogo esta turma representa?
    treinamento_id = db.Column(db.Integer, db.ForeignKey(
        'treinamentos.id'), nullable=False)

    # 2. Quem é o instrutor desta turma? (Supondo que você tenha um modelo Instrutor)
    # instrutor_id = db.Column(db.Integer, db.ForeignKey('instrutores.id'), nullable=False)

    # --- Propriedades de Navegação ---

    # Relação para que, a partir de uma Turma, você possa saber quais alunos estão inscritos.
    alunos = db.relationship('Aluno', backref='turma', lazy='dynamic')

    def __repr__(self):
        # Acessa o nome do treinamento através da relação 'treinamento'
        # (que será criada no modelo Treinamento)
        nome = self.treinamento.nome_treinamento if self.treinamento else 'N/A'
        return f'<Turma {self.id}: {nome} em {self.data_inicio}>'

    def to_dict(self):
        return {
            'id': self.id,
            'treinamento_id': self.treinamento_id,
            'data_inicio': self.data_inicio.isoformat(),  # Formato padrão para JSON
            'horario': self.horario,
            'local': self.local,
            'status': self.status,
            # Você pode até incluir informações do treinamento relacionado
            'treinamento_info': self.treinamento.to_dict() if self.treinamento else None
        }
