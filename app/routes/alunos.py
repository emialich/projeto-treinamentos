from flask import Blueprint, jsonify, request
from app.models.alunos import Aluno
from app.models.turmas import Turma
from app.database import db

alunos_bp = Blueprint('alunos_bp', __name__, url_prefix='/alunos')


@alunos_bp.route('/', methods=['GET'])
def get_alunos():
    """
    Obtém todos os alunos ou, se um 'turma_id' for fornecido, filtra por essa
    turma e enriquece a resposta com o nome do treinamento e do instrutor.
    """
    # 1. Tenta obter o 'turma_id' dos argumentos da URL
    turma_id_filtro = request.args.get('turma_id', type=int)

    # --- CASO 1: A ROTA É FILTRADA POR TURMA ---
    if turma_id_filtro:
        # Busca o objeto Turma completo pelo ID fornecido.
        # Esta é a abordagem mais eficiente.
        turma = Turma.query.get(turma_id_filtro)

        # Se a turma com o ID especificado não for encontrada, retorna um erro 404.
        if not turma:
            return jsonify({"erro": f"A turma com ID {turma_id_filtro} não foi encontrada."}), 404

        # Acessa os dados relacionados através das relações do SQLAlchemy
        # Isso só é possível se os 'relationships' estiverem definidos nos seus modelos.
        nome_treinamento = turma.treinamento.nome_treinamento if turma.treinamento else "N/A"
        instrutor_sugerido = turma.treinamento.instrutor_sugerido if turma.treinamento else "N/A"

        # Pega a lista de alunos diretamente do objeto turma
        alunos_da_turma = [aluno.to_dict() for aluno in turma.alunos]

        # Monta o objeto de resposta JSON com a estrutura especial
        resposta_filtrada = {
            "nome_treinamento": nome_treinamento,
            "instrutor_sugerido": instrutor_sugerido,
            "alunos": alunos_da_turma
        }

        return jsonify(resposta_filtrada)

    # --- CASO 2: A ROTA NÃO É FILTRADA ---
    else:
        # Se nenhum filtro foi passado, retorna a lista simples de todos os alunos.
        alunos = Aluno.query.all()
        return jsonify([aluno.to_dict() for aluno in alunos])


@alunos_bp.route('/', methods=['POST'])
def create_aluno():
    """
    Cria um novo aluno e o associa a uma TURMA específica.
    """
    dados = request.get_json()

    if not dados or 'nome' not in dados or 'email' not in dados or 'turma_id' not in dados:
        return jsonify({"erro": "Dados incompletos. 'nome', 'email' e 'turma_id' são obrigatórios."}), 400

    # 1. Receber o ID da turma
    turma_id = dados.get('turma_id')

    # 2. Validar se a turma existe
    turma_existente = Turma.query.get(turma_id)
    if not turma_existente:
        return jsonify({"erro": f"A turma com ID {turma_id} não foi encontrada."}), 404
        #

    # 3. Validação extra (opcional, mas recomendada): Verificar se a turma não está cheia
    # if len(turma_existente.alunos) >= turma_existente.limite_vagas:
    #     return jsonify({"erro": "Esta turma já atingiu o limite de vagas."}), 409 # Conflict

    try:
        # 4. Criar o Objeto Aluno associado à turma
        novo_aluno = Aluno(
            nome=dados['nome'],
            email=dados['email'],
            turma_id=turma_id,
            pago=dados.get('pago', False)
        )

        db.session.add(novo_aluno)
        db.session.commit()

        return jsonify(novo_aluno.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        # Verificar se o erro é de violação de unicidade (email duplicado)
        if 'UNIQUE constraint failed' in str(e) or 'duplicate key value' in str(e):
            return jsonify({"erro": f"O email '{dados['email']}' já está cadastrado."}), 409

        return jsonify({"erro": f"Não foi possível criar o aluno: {str(e)}"}), 500


@alunos_bp.route('/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio"}), 400

    if 'nome' in dados:
        aluno.nome = dados['nome']
    if 'email' in dados:
        aluno.email = dados['email']
    if 'pago' in dados:
        aluno.pago = dados['pago']

    db.session.commit()

    return jsonify(aluno.to_dict())


@alunos_bp.route('/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()

    return jsonify({"mensagem": "Aluno excluído com sucesso"}), 200
