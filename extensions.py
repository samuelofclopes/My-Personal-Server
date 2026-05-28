from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_limiter import Limiter


# Instancias:
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
limiter = Limiter(lambda: request.headers.get("CF-Connecting-IP", request.remote_addr),storage_uri="memory://")