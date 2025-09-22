from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db  # Importa a instância central do SQLAlchemy

# Importa os modelos necessários
from app.models.treinamentos import Treinamento
from app.models.turmas import Turma

# Criação do blueprint
treinamentos_bp = Blueprint(
    'treinamentos', __name__, url_prefix='/treinamentos')

# --- Rotas do CATÁLOGO de Treinamentos ---


@treinamentos_bp.route('', methods=['GET'])
def obter_treinamentos():
    """
    Obtém todos os treinamentos do CATÁLOGO.
    """
    treinamentos = Treinamento.query.order_by(
        Treinamento.nome_treinamento).all()
    return jsonify([t.to_dict() for t in treinamentos])


# Importa os modelos necessários
# Criação do blueprint
treinamentos_bp = Blueprint(
    'treinamentos', __name__, url_prefix='/treinamentos')

# --- Rotas do CATÁLOGO de Treinamentos ---


@treinamentos_bp.route('', methods=['GET'])
def obter_treinamentos():
    """Obtém todos os treinamentos do CATÁLOGO."""
    treinamentos = Treinamento.query.order_by(
        Treinamento.nome_treinamento).all()
    return jsonify([t.to_dict() for t in treinamentos])

# --- NOVA ROTA: Listar por Instrutor ---


@treinamentos_bp.route('/instrutor/<string:nome_instrutor>', methods=['GET'])
def obter_treinamentos_por_instrutor(nome_instrutor):
    """
    Obtém os treinamentos do CATÁLOGO filtrados por um instrutor específico.
    """
    # A busca é case-insensitive para melhorar a experiência do usuário
    treinamentos = Treinamento.query.filter(
        Treinamento.instrutor_sugerido.ilike(f"%{nome_instrutor}%")
    ).all()

    if not treinamentos:
        return jsonify({"mensagem": "Nenhum treinamento encontrado para este instrutor"}), 404

    return jsonify([t.to_dict() for t in treinamentos])


@treinamentos_bp.route('', methods=['DELETE'])
def remover_treinamento_catalogo():
    """
    Remove um treinamento do catálogo com base no ID e nome fornecidos
    no corpo (JSON) da requisição.
    """
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição não pode estar vazio"}), 400

    # Passo 1: Obter ID e nome do corpo da requisição
    treinamento_id = dados.get('id')
    nome_para_validacao = dados.get('nome_treinamento')

    if not treinamento_id or not nome_para_validacao:
        return jsonify({"erro": "Os campos 'id' e 'nome_treinamento' são obrigatórios no corpo da requisição."}), 400

    # Passo 2: Busca o treinamento pelo ID fornecido no corpo
    treinamento = Treinamento.query.get(treinamento_id)
    if not treinamento:
        return jsonify({"erro": f"Treinamento com ID {treinamento_id} não encontrado."}), 404

    # Passo 3: Validação cruzada
    if treinamento.nome_treinamento != nome_para_validacao:
        return jsonify({
            "erro": "Validação falhou. O nome do treinamento não corresponde ao ID fornecido.",
            "detalhe": f"O treinamento com ID {treinamento_id} se chama '{treinamento.nome_treinamento}', mas foi fornecido '{nome_para_validacao}'."
        }), 400

    # Validação extra de negócio: Não permitir remover se houver turmas
    if treinamento.turmas:
        # 409 Conflict
        return jsonify({"erro": "Não é possível remover um treinamento que já possui turmas agendadas."}), 409

    try:
        # Passo 4: Remoção
        db.session.delete(treinamento)
        db.session.commit()
        return jsonify({"mensagem": f"Treinamento '{treinamento.nome_treinamento}' removido com sucesso."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Ocorreu um erro ao remover o treinamento: {str(e)}"}), 500


@treinamentos_bp.route('', methods=['POST'])
def criar_treinamento_catalogo():
    """
    Cria um novo TREINAMENTO no catálogo.
    Não cria uma turma, apenas o item que pode ser agendado.
    """
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição não pode estar vazio"}), 400

    # Validação dos campos obrigatórios
    if 'nome_treinamento' not in dados or 'vendor' not in dados:
        return jsonify({"erro": "Campos 'nome_treinamento' e 'vendor' são obrigatórios"}), 400

    try:
        # Cria a nova instância do Treinamento
        novo_treinamento = Treinamento(
            nome_treinamento=dados['nome_treinamento'],
            vendor=dados['vendor'],
            # .get() para campo opcional
            instrutor_sugerido=dados.get('instrutor_sugerido')
        )

        # Adiciona e salva no banco de dados
        db.session.add(novo_treinamento)
        db.session.commit()

        # Retorna o objeto criado com o status 201 Created
        return jsonify(novo_treinamento.to_dict()), 201

    except Exception as e:
        db.session.rollback()  # Desfaz a transação em caso de erro
        return jsonify({"erro": f"Ocorreu um erro ao criar o treinamento: {str(e)}"}), 500


@treinamentos_bp.route('/<string:vendor>', methods=['GET'])
def obter_treinamentos_por_vendor(vendor):
    """
    Obtém os treinamentos do CATÁLOGO filtrados por um vendor.
    """
    treinamentos = Treinamento.query.filter_by(vendor=vendor).all()
    if not treinamentos:
        return jsonify({"mensagem": "Nenhum treinamento encontrado para este vendor"}), 404
    return jsonify([t.to_dict() for t in treinamentos])


# --- Rotas de TURMAS (Agendamentos) ---

@treinamentos_bp.route('/agendados', methods=['GET'])
def obter_treinamentos_agendados():
    """
    Obtém todas as TURMAS com data de início futura.
    """
    hoje = datetime.today().date()
    turmas_agendadas = Turma.query.filter(
        Turma.data_inicio >= hoje).order_by(Turma.data_inicio).all()
    return jsonify([turma.to_dict() for turma in turmas_agendadas])


@treinamentos_bp.route('/agendados', methods=['POST'])
def agendar_treinamento():
    """
    Cria uma nova TURMA (agenda um treinamento do catálogo).
    """
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio"}), 400

    try:
        treinamento_id = dados['treinamento_id']
        data_inicio_str = dados['data_inicio']

        treinamento_catalogo = Treinamento.query.get(treinamento_id)
        if not treinamento_catalogo:
            return jsonify({"erro": f"O treinamento com ID {treinamento_id} não existe no catálogo"}), 404

        nova_turma = Turma(
            treinamento_id=treinamento_id,
            data_inicio=datetime.fromisoformat(data_inicio_str).date(),
            horario=dados.get('horario'),
            local=dados.get('local'),
            status=dados.get('status', 'Agendada')
        )

        db.session.add(nova_turma)
        db.session.commit()

        return jsonify(nova_turma.to_dict()), 201

    except KeyError as e:
        return jsonify({"erro": f"Campo obrigatório ausente: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Ocorreu um erro: {str(e)}"}), 500


@treinamentos_bp.route('/agendados/<int:turma_id>', methods=['PUT'])
def atualizar_treinamento_agendado(turma_id):
    """
    Atualiza uma TURMA existente (ex: para cancelar).
    """
    turma_para_atualizar = Turma.query.get(turma_id)
    if not turma_para_atualizar:
        return jsonify({"erro": "Turma não encontrada"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio"}), 400

    if 'status' in dados:
        turma_para_atualizar.status = dados['status']
    if 'data_inicio' in dados:
        turma_para_atualizar.data_inicio = datetime.fromisoformat(
            dados['data_inicio']).date()
    if 'local' in dados:
        turma_para_atualizar.local = dados['local']

    db.session.commit()

    return jsonify(turma_para_atualizar.to_dict())
