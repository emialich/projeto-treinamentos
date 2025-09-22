from app.database import db


class Aluno(db.Model):
    """
    Representa um aluno inscrito em uma TURMA específica.
    """
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pago = db.Column(db.Boolean, nullable=False, default=False)
    # Isso conecta o aluno a um agendamento específico.
    turma_id = db.Column(db.Integer, db.ForeignKey(
        'turmas.id'), nullable=False)

    def __repr__(self):
        return f'<Aluno {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'pago': self.pago,
            'turma_id': self.turma_id
        }
