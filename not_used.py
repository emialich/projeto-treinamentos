# Importação das bibliotecas necessárias do Flask
from flask import Flask, jsonify, request

# Criamos uma instância da classe Flask
# __name__ é uma variável especial que representa o nome do módulo atual
app = Flask(__name__)

# Lista que simula um banco de dados em memória
# Contém os dados dos livros que serão manipulados pela API
livros = [
    {
        'id': 1,
        'titulo': 'Data Science com Python',
        'autor': 'Joel Rus'
    },
    {
        'id': 2,
        'titulo': 'A história de quem fica e quem foge',
        'autor': 'Helena Ferrante'
    },
    {
        'id': 3,
        'titulo': 'Vinte Mil Leguas Submarinas',
        'autor': 'Julio Verne'
    },
]

# ROTA 1: Consultar todos os livros
# Método GET na URL /livros retorna toda a lista de livros


@app.route('/treinamentos', methods=['GET'])
def obter_livros():
    # jsonify() converte a lista Python em formato JSON para envio
    return jsonify(livros)

# ROTA 2: Consultar um livro específico por ID
# <int:id> captura o ID da URL como um parâmetro inteiro


@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):
    # Percorre a lista de livros procurando pelo ID correspondente
    for livro in livros:
        if livro.get('id') == id:
            # Retorna o livro encontrado em formato JSON
            return jsonify(livro)
    # Se não encontrar o livro, retorna None (seria melhor retornar erro 404)

# ROTA 3: Editar/Atualizar um livro existente por ID
# Método PUT é usado para atualizações completas


@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro_por_id(id):
    # Recupera os dados JSON enviados no corpo da requisição
    livro_alterado = request.get_json()

    # Percorre a lista usando enumerate para obter índice e valor
    for indice, livro in enumerate(livros):
        if livro.get('id') == id:
            # update() mescla os novos dados com os existentes
            livros[indice].update(livro_alterado)
            # Retorna o livro atualizado
            return jsonify(livros[indice])

# ROTA 4: Criar um novo livro
# ATENÇÃO: Esta rota tem um problema - não deveria usar ID na URL para criação
# O método POST geralmente usa apenas /livros sem ID


@app.route('/livros/<int:id>', methods=['POST'])
def criar_livro_por_id(id):
    # Obtém os dados do novo livro do corpo da requisição
    novo_livro = request.get_json()
    # Adiciona o novo livro à lista
    livros.append(novo_livro)
    # Retorna toda a lista atualizada (seria melhor retornar apenas o novo livro)
    return jsonify(livros)

# ROTA 5: Excluir um livro por ID
# Método DELETE remove o recurso especificado


@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro_por_id(id):
    # Percorre a lista procurando o livro a ser deletado
    for indice, livro in enumerate(livros):
        if livro.get('id') == id:
            # Remove o livro da lista usando seu índice
            del livros[indice]
            # Retorna a lista atualizada (seria melhor retornar status de sucesso)
            return jsonify(livros)


# Inicia o servidor Flask
# port=5000: define a porta onde a aplicação será executada
# host='localhost': define que aceita conexões apenas localmente
# debug=True: ativa o modo debug com recarregamento automático e mensagens detalhadas
app.run(port=5000, host='localhost', debug=True)
