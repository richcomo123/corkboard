import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from corkboard.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from corkboard.routes import main
    app.register_blueprint(main)

    # Update the file_type function
    def file_type(filename):
        _, extension = os.path.splitext(filename)
        if extension.lower() in ('.jpg', '.jpeg', '.png', '.gif'):
            return 'image'
        elif extension.lower() in ('.mp4', '.avi', '.mkv'):
            return 'video'
        elif extension.lower() == '.pdf':
            return 'pdf'
        elif extension.lower() == '.docx':
            return 'docx'
        else:
            return 'other'

    # Add the file_type filter to the Jinja environment
    app.jinja_env.filters['file_type'] = file_type

    from corkboard import routes

    return app


