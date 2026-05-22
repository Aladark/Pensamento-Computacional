from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__, template_folder="src/templates")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "chave-secreta-desenvolvimento")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///academico.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "info"

    from src.auth.routes import auth_bp
    from src.disciplinas.routes import disciplinas_bp
    from src.notas.routes import notas_bp
    from src.recomendacoes.routes import recomendacoes_bp
    from src.relatorios.routes import relatorios_bp
    from src.main.routes import main_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(disciplinas_bp, url_prefix="/disciplinas")
    app.register_blueprint(notas_bp, url_prefix="/notas")
    app.register_blueprint(recomendacoes_bp, url_prefix="/recomendacoes")
    app.register_blueprint(relatorios_bp, url_prefix="/relatorios")
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        from src.seed import seed_data
        seed_data()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
