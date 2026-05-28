from flask import Blueprint, request, current_app, jsonify
from extensions import db
from models.user import User
from mail_sender import send_mail
from auth.validators import password_valida, email_valido, username_valido, confirm_password, have_all_data
from itsdangerous import BadSignature, SignatureExpired
auth = Blueprint("auth", __name__)


@auth.route("/api/auth/signup", methods=["POST"])
def signup():
    # Obter os dados do pedido
    dados = request.get_json()

    # Pegar os dados necessários e validar cada um deles
    # Assegurar que os dados necessários estão presentes
    have_all_data_result = have_all_data(dados, "signup")
    if not dados or not have_all_data_result[0]:
        return {"message": have_all_data_result[1]}, 400
    

    password_valida_result = password_valida(dados.get("password")) 
    if not password_valida_result[0]:
        return {"message": password_valida_result[1]}, 400
    

    email_valido_result = email_valido(dados.get("email"))
    if not email_valido_result[0]:
        return {"message": email_valido_result[1]}, 400


    username_valido_result = username_valido(dados.get("username"))
    if not username_valido_result[0]:
        return {"message": username_valido_result[1]}, 400


    confirm_password_result = confirm_password(dados.get("password"), dados.get("confirm_password"))
    if not confirm_password_result[0]:
        return {"message": confirm_password_result[1]}, 400


    # Crirar o token de verificação
    token = current_app.serializer.dumps({"username": dados.get("username")}, salt="confirmar-email")

    # Criar o utilizador, guardar na base de dados
    novo_user = User(
        username=dados.get("username"),
        email=dados.get("email"),
        v_code=token
    )
    novo_user.set_password(dados.get("password"))
    db.session.add(novo_user)
    db.session.commit()

    # Enviar email de verificação
    send_mail(
        email=novo_user.email,
        code=novo_user.v_code,
        user_id=novo_user.id
    )

    # Retornar resposta de sucesso
    return jsonify({
        "message": "Utilizador registado com sucesso",
        "user": {
            "id": novo_user.id,
            "username": novo_user.username,
            "email": novo_user.email,
            "created_at": novo_user.created_at.isoformat()
        }
    }), 201