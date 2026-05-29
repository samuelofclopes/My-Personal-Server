import os
from flask import Flask
from itsdangerous import URLSafeTimedSerializer
from extensions import db, jwt, migrate, limiter
from routes.auth import auth as auth_bp

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
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)