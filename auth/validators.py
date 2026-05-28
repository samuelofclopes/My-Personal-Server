from email_validator import validate_email, EmailNotValidError
from models.user import User

def username_valido(username):
    if len(username) < 3 or len(username) > 20:
        return False, "Username deve ter entre 3 e 20 caracteres."
    if not any(c.isalpha() for c in username):
        return False, "Username deve conter pelo menos uma letra."
    if User.query.filter_by(username= username).first():
        return False, "Username já existe."
    return True, "ok"

def email_valido(email):
    try:
        email_info = validate_email(email, check_deliverability=False)
        if User.query.filter_by(email= email_info.normalized).first():
            return False, "Email já existe."
        return True, email_info.normalized  # Retorna o email normalizado (limpo)
    except EmailNotValidError as e:
        # O email é inválido ou o domínio não existe
        return False, "Email inválido."

def password_valida(password):
    if len(password) < 6:
        return False, "Password deve ter pelo menos 6 caracteres."
    if not any(c.isalpha() for c in password):
        return False, "Password deve conter pelo menos uma letra."
    if not any(c.isdigit() for c in password):
        return False, "Password deve conter pelo menos um número."
    return True, "ok"

def confirm_password(password, confirm_password):
    if password == confirm_password:
        return True, "ok"
    else:
        return False, "Passwords não coincidem."

def have_all_data(data, purpose):
    if not data:
        return False, "Dados em falta."
    if not data.get("username"):
        return False, "Username é obrigatório."
    if not data.get("password"):
        return False, "Password é obrigatório."

    if purpose == "signup":
        if not data.get("email"):
            return False, "Email é obrigatório."
        if not data.get("confirm_password"):
            return False, "Confirmação de password é obrigatória."
        
    return True, "ok"
    
