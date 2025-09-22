from app.database import db


class Treinamento(db.Model):
    """
    Representa um treinamento do CATÁLOGO de cursos da empresa.
    Não representa um evento agendado.
    """

    __tablename__ = 'treinamentos'

    id = db.Column(db.Integer, primary_key=True)
    nome_treinamento = db.Column(db.String(150), nullable=False)
    vendor = db.Column(db.String(100), nullable=False)

    # Este campo pode sair daqui e ir para a Turma, se cada turma
    # puder ter um instrutor diferente. Vou mantê-lo aqui como sugestão.
    instrutor_sugerido = db.Column(db.String(150), nullable=True)

    # --- RELAÇÃO ALTERADA ---
    # A relação com 'Aluno' foi removida.
    # Em seu lugar, esta relação permite encontrar todas as turmas de um treinamento.
    # Ex: curso_python.turmas -> [<Turma 1>, <Turma 2>, ...]
    turmas = db.relationship('Turma', backref='treinamento', lazy=True)

    def __repr__(self):
        return f'<Treinamento (Catálogo) {self.nome_treinamento}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome_treinamento': self.nome_treinamento,
            'vendor': self.vendor,
            'instrutor_sugerido': self.instrutor_sugerido
        }
