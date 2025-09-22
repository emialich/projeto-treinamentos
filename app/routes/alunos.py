from flask import Blueprint, jsonify, request
from app.models.alunos import Aluno  # Importa o modelo
from app.models.treinamentos import Treinamento  # Importa o modelo
from app.database import db  # Importa a sessão do DB

alunos_bp = Blueprint('alunos_bp', __name__)


@alunos_bp.route('/', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    # Converte a lista de objetos para um formato JSON
    return jsonify([{'id': aluno.id, 'nome': aluno.nome, 'email': aluno.email} for aluno in alunos])


@alunos_bp.route('/', methods=['POST'])
def create_aluno():
    # Aqui você pegaria os dados da requisição (request.json)
    # Exemplo simplificado:
    # Pega os dados JSON enviados na requisição
    dados = request.get_json()

    if not dados or not 'nome' in dados or not 'email' in dados:
        return jsonify({"erro": "Dados incompletos"}), 400

    treinamento_id = dados.get('treinamento_id')
    # 3. Consulta o banco para ver se o treinamento existe
    treinamento_existente = Treinamento.query.get(treinamento_id)

    # 4. Se não existir, lança um erro
    if not treinamento_existente:
        # A mensagem de erro será capturada pelo 'try...except' na rota
        raise ValueError(
            f"O treinamento com ID {treinamento_id} não foi encontrado.")

    try:
        # Chama o serviço para criar o aluno no banco
        # 1. Criar o Objeto em Memória
        novo_aluno = Aluno(
            nome=dados['nome'],
            email=dados['email'],
            treinamento_id=dados['treinamento_id'],
            pago=dados.get('pago', False)
        )

        # 2. Adicionar à Sessão (Área de Preparação)
        db.session.add(novo_aluno)

        # 3. Confirmar a Transação (Salvar no Banco)
        db.session.commit()

        # Usa o método to_dict() para converter o objeto em dicionário
        # e retorna como JSON com o status 201 (Created)
        return jsonify(novo_aluno.to_dict()), 201

    except Exception as e:
        # Em caso de erro (ex: email duplicado), retorna um erro genérico
        db.session.rollback()  # Desfaz a transação
        return jsonify({"erro": f"Não foi possível criar o aluno: {str(e)}"}), 500
