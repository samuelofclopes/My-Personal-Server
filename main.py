import os
from flask import Flask
from itsdangerous import URLSafeTimedSerializer
from extensions import db, jwt, migrate, limiter
from routes.auth import auth as auth_bp
from routes.moral import moral as moral_bp
from routes.frontend import frontend as frontend_bp
from dotenv import load_dotenv

# Pega as variáveis de ambiente do ficheiro .env
load_dotenv()



# create_app é a função que retorna toda a aplicação e as suas extenções.
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY")
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    app.serializer = URLSafeTimedSerializer(os.getenv("JWT_KEY"))
    app.register_blueprint(auth_bp)
    app.register_blueprint(moral_bp)
    app.register_blueprint(frontend_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)