from flask import Blueprint, request, current_app, jsonify, redirect
from extensions import db, limiter
from models.user import User
from mail_sender import send_mail, send_recovery_mail
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from auth.validators import password_valida, email_valido, username_valido, confirm_password, have_all_data
from itsdangerous import BadSignature, SignatureExpired
auth = Blueprint("auth", __name__)


"""
Esta rota é responsável por registar um novo utilizador, validar os dados fornecidos,
criar um token de verificação, guardar o utilizador na base de dados e enviar um email de verificação.

"""
@auth.route("/api/auth/signup", methods=["POST"])
@limiter.limit("30 per minute")
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



"""
Esta rota é resposável por fazer o login no servidor, validar os dados fornecidos,
verificar se o utilizador existe e se a password está correta.
"""
@auth.route("/api/auth/signin", methods=["POST"])
@limiter.limit("30 per minute")
def signin():
    # Obter os dados do pedido
    dados = request.get_json()

    # Pegar os dados necessários e validar cada um deles
    # Assegurar que os dados necessários estão presentes
    have_all_data_result = have_all_data(dados, "signin")
    if not dados or not have_all_data_result[0]:
        return {"message": have_all_data_result[1]}, 400
    


    # Verificar se o utilizador existe e se a password está correta
    user = User.query.filter_by(email=dados.get("email")).first()
    if not user or not user.check_password(dados.get("password")):
        return {"message": "Email ou password incorretos"}, 401

    # Verificar se o email do utilizador está verificado
    if not user.email_v:
        return {"message": "Email não verificado. Por favor, verifique seu email antes de fazer login."}, 403
    
    # Criar o token de acesso
    token = create_access_token(identity=str(user.id))

    # Retornar resposta de sucesso
    return jsonify({
        "message": "Login bem sucedido",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat(),
        }
    }), 200



"""
Esta rota é responsável por retornar os dados do utilizador,
para isso, ele precisa de um token de acesso dado pelo login.
"""
@auth.route("/api/auth/user", methods=["GET"])
@limiter.limit("30 per minute")
@jwt_required()
def get_user():
    # Obter o token de acesso do header Authorization
    user = User.query.get(get_jwt_identity())

    if not user:
        return {"message": "Utilizador não encontrado"}, 404




    # Retornar os dados do utilizador
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 200



"""
Esta rota é responsável por verificar o email do utilizador,
para isso, ele precisa de dados de verificação vindos do email.
"""
@auth.route("/api/auth/confirm_email/<string:token>", methods=["POST"])
@limiter.limit("30 per minute")
def confirm_email(token):
    

    # Verificar se o código de verificação é válido e não expirou usando try except para controlar os erros.
    try:
        token_username = current_app.serializer.loads(token, salt="confirmar-email", max_age=14400).get("username")

    except SignatureExpired:
        return {"message": "Codigo de verificação expirado"}, 400
    
    except BadSignature:
        return {"message": "Codigo de verificação inválido"}, 400


    # Pegar o utilizador da base de dados e verificar se ele existe
    user = User.query.filter_by(username=token_username).first()
    if not user:
        return {"message": "Utilizador não encontrado"}, 404
    

    # Verificar o código de verificação
    user.email_v = True
    db.session.commit()

    # Retornar resposta de sucesso
    return {"message": "Email verificado com sucesso"}, 200




"""
Esta rota é responsavel por enviar um email de recuperação de password,
para isso, ele precisa do email do utilizador.
"""
@auth.route("/api/auth/forgot_password", methods=["POST"])
@limiter.limit("30 per minute")
def forgot_password():

    # Obter os dados do pedido
    dados = request.get_json()


    # Verificar se o utilizador existe e se os dados extão presentes
    if not dados or not dados.get("email"):
        return {"message": "Email não fornecido"}, 400

    user = User.query.filter_by(email=dados.get("email")).first()
    if not user:
        return {"message": "Verifica a caixa de entrada do email."}, 400


    # Criar o token de recuperação de password
    token = current_app.serializer.dumps({"username": user.username}, salt="recuperar-password")


    # Enviar email de recuperação de password
    send_recovery_mail(
        email=user.email,
        code=token,
    )


    # Retornar resposta de sucesso
    return {"message": "Verifica a caixa de entrada do email."}, 200




"""
Esta rota é responsável por recuperar a password do utilizador,
para isso, ele precisa de dados de recuperação de password vindos do email.
"""
@auth.route("/api/auth/reset_password/<string:token>", methods=["GET","POST"])
@limiter.limit("30 per minute")
def reset_password(token):

    # Verificar se o código de recuperação de password é válido e não expirou usando try except para controlar os erros.
    try:
        token_username = current_app.serializer.loads(token, salt="recuperar-password", max_age=3600).get("username")
    except SignatureExpired:
        return {"message": "Codigo de recuperação de password expirado"}, 400
    except BadSignature:
        return {"message": "Codigo de recuperação de password inválido"}, 400
    


    # Se o método for GET, redirecionar para a página de reset de password.
    if request.method == "GET":
        return redirect(f"/reset_password?token={token}")
    

    # Obter os dados do pedido
    dados = request.get_json()



    # Verificar se os dados estão presentes e se a password é válida
    if not dados or not dados.get("password") or not dados.get("confirm_password"):
        return {"message": "Dados incompletos"}, 400
    


    # Verificar se a pass nova é valida e se as duas passwords condizem.
    password_valida_result = password_valida(dados.get("password"))
    if not password_valida_result[0]:
        return {"message": password_valida_result[1]}, 400
    
    confirm_password_result = confirm_password(dados.get("password"), dados.get("confirm_password"))
    if not confirm_password_result[0]:
        return {"message": confirm_password_result[1]}, 400
    
    
    # verificar se utilizador existe
    user = User.query.filter_by(username=token_username).first()
    if not user:
        return {"message": "Codigo de recuperação de password inválido"}, 400


    # Atualizar a password do utilizador
    user.set_password(dados.get("password"))
    db.session.commit()

    return {"message": "Password atualizada com sucesso"}, 200