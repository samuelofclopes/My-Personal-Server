from email_validator import validate_email, EmailNotValidError
from models.user import User
import string
import hashlib
import requests



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
    # Regras básicas (rápidas, sem rede necessária)
    if len(password) < 8:
        return False, "Password deve ter pelo menos 8 caracteres."
    if not any(c.isalpha() for c in password):
        return False, "Password deve conter pelo menos uma letra."
    if not any(c.isdigit() or c in string.punctuation for c in password):
        return False, "Password deve conter pelo menos um número ou um caractere especial."

    # Verificar se a password já apareceu em fugas de dados (Have I Been Pwned)
    # Calculamos o hash SHA-1 e enviamos só os 5 primeiros caracteres.
    # A password (e o hash completo) nunca saem do servidor.
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefixo, resto = sha1[:5], sha1[5:]

    try:
        resposta = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefixo}",
            headers={"User-Agent": "My-Personal-Server"},  # a API exige este cabeçalho
            timeout=3,                                      # não ficar à espera para sempre
        )
        resposta.raise_for_status()

        # A API devolve linhas "SUFIXO:vezes". Se o nosso sufixo estiver lá, a password foi vazada.
        for linha in resposta.text.splitlines():
            sufixo, _, vezes = linha.partition(":")
            if sufixo == resto:
                return False, "Esta password apareceu em fugas de dados. Escolhe outra."

    except requests.RequestException:
        pass  # API indisponível: deixamos passar (decisão: disponibilidade > verificação)

    return True, "ok"

def confirm_password(password, confirm_password):
    if password == confirm_password:
        return True, "ok"
    else:
        return False, "Passwords não coincidem."

def have_all_data(data, purpose):

    
    if not data:
        return False, "Dados em falta."
    if not isinstance(data, dict):
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
    
