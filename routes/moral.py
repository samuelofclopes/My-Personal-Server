from flask import Blueprint, request, jsonify
from extensions import db, limiter
from models.user import User
from models.messages import Message     
from flask_jwt_extended import get_jwt_identity, jwt_required
moral = Blueprint("moral", __name__)


"""
Esta rota é responsável por retornar as últimas 50 mensagens do moral,
ela pega as mensagens da base de dados, ordena por id decrescente e retorna as 50 primeiras (LIFO - Last In, First Out) como uma pilha
"""
@moral.route("/api/moral", methods=["GET"])
@limiter.limit("50 per minute")
def get_moral():

    # Fazer query á db para pegar as mensagens
    moral = Message.query.order_by(Message.id.desc()).limit(50).all() # Ordenar por id decrescente, pega todas com limite de 50

    # Retornar as 50 mensagens dentro de uma lista
    return jsonify({
        "mensagens": [
            {"id": m.id,
             "user": m.user,
             "content": m.content,
             "created_at": m.created_at.isoformat
             ()} for m in moral # m é a mensagem, o moral é o numero de mensagens
        ]
    }), 200


"""
Esta rota é responsável por adicionar um comentário ao moral,
ela pega o comentário do corpo do pedido e o id do utilizador do token de acesso,
verifica se o token é válido, e se sim, cria um novo comentário e guarda na base de dados
"""
@moral.route("/api/moral/comentarios", methods=["POST"])
@limiter.limit("20 per minute")
@jwt_required()
def add_comentario():
    # Obter os dados do pedido e o id do utilizador do token de acesso
    data = request.get_json()
    user_id = get_jwt_identity()
        

    # Procura o utilizador para verificar se o token é valido
    user = User.query.get(user_id)
    

    # Se não existe, retorna erro
    if not user:
        return jsonify({"error": "Utilizador não encontrado."}), 404 
    

    # Cria o nove comentário
    novo_comentario = Message(
        user=user.username,
        content=data.get("content")
    )


    # Adiciona o comentário à base de dados
    db.session.add(novo_comentario)
    db.session.commit()

    # Retorna resposta de sucesso
    return jsonify({"message": "Comentário adicionado com sucesso."}), 201