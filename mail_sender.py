import resend
import os

resend.api_key = os.getenv("RESEND_KEY")

def send_mail(email, code):
    try:
        r = resend.Emails.send({
            "from": "noreply@moita.uk",
            "to": email,
            "subject": "Verificação 2FA - Moita's Server",
            "html": f"<p>Segue este link para verificar a tua conta: <strong>https://moita.uk/api/auth/confirm_email/{code}</strong></p>"
        })
        print(f"Email enviado com sucesso - ID: {r['id']}")
    except Exception as e:
        print(f"Erro ao enviar email via Resend: {e}")


def send_recovery_mail(email, code):
    try:
        r = resend.Emails.send({
            "from": "noreply@moita.uk", 
            "to": email,
            "subject": "Recuperação de Password - Moita's Server",
            "html": f"<p>Segue este link para recuperar a tua password: <strong>https://moita.uk/api/auth/reset_password/{code}</strong></p>"
        })
        print(f"Email enviado com sucesso - ID: {r['id']}")
    except Exception as e:
        print(f"Erro ao enviar email via Resend: {e}")
