from flask import render_template, Blueprint, request
frontend = Blueprint("frontend", __name__)



"""
Esta rota é responsável por renderizar a página principal do site,
onde o moral é exibido
"""
@frontend.route("/")
def landing_page():
    return render_template("/public/landing_page.html")



"""
Esta rota é responsável por renderizar a página de registo,
onde os utilizadores podem criar uma nova conta
"""
@frontend.route("/signup")
def signup():
    return render_template("/public/signup.html")



"""
Esta rota é responsável por renderizar a página de login,
onde os utilizadores podem entrar com as suas credenciais
"""
@frontend.route("/login")
def login():
    return render_template("/public/login.html")



"""
Esta rota é responsável por renderizar a pagina de dashboard, 
onde os utilizadores podem ver o seu perfil, editar as suas informações e aceder a outras funcionalidades
"""
@frontend.route("/dashboard")
def dashboard():
    return render_template("/private/dashboard.html")



"""
Esta rota é responsável por renderizar a página de perfil, 
onde os utilizadores podem ver o seu perfil e editar as suas informações
"""
@frontend.route("/profile")
def profile():
    return render_template("/private/profile.html")



"""
Esta rota é responsável por renderizar a pagina de "Forgot Password",
onde os utilizadores podem solicitar uma redefinição de senha
"""
@frontend.route("/forgot_password")
def forgot_password():
    return render_template("/public/forgot_password.html")



"""
Esta rota é responsável por renderizar a página de "Reset Password",
onde os utilizadores podem redefinir a sua senha após solicitar uma redefinição
"""
@frontend.route("/reset_password")
def reset_password():
    token = request.args.get("token")
    return render_template("/public/reset_password.html", token=token)