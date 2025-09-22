from flask import Blueprint, jsonify, request
from app.models.alunos import Aluno  # Importa o modelo Aluno
from app.models.turmas import Turma    # <<-- MUDANÇA: Importa o modelo Turma
from app.database import db          # Importa a sessão do DB

# O prefixo da URL faz mais sentido ser /alunos, mas vou manter o seu para consistência
# Se quiser, pode mudar para:
alunos_bp = Blueprint('alunos_bp', __name__, url_prefix='/alunos')
# alunos_bp = Blueprint('alunos_bp', __name__, url_prefix='/agendamentos')


@alunos_bp.route('/', methods=['GET'])
def get_alunos():
    """
    Obtém todos os alunos ou filtra os alunos por turma_id.
    O filtro é passado como um argumento na URL, ex: /alunos?turma_id=1
    """
    # 1. Tenta obter o 'turma_id' dos argumentos da URL
    turma_id_filtro = request.args.get('turma_id', type=int)

    # 2. Se um turma_id foi fornecido na URL, filtra por ele
    if turma_id_filtro:
        alunos = Aluno.query.filter_by(turma_id=turma_id_filtro).all()
        # Se nenhum aluno for encontrado para essa turma, você pode querer retornar uma lista vazia ou uma mensagem
        if not alunos:
            return jsonify({"mensagem": f"Nenhum aluno encontrado para a turma de ID {turma_id_filtro}"}), 404

    # 3. Se nenhum turma_id foi fornecido, retorna todos os alunos
    else:
        alunos = Aluno.query.all()

    # 4. Retorna a lista de alunos (filtrada ou não)
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
