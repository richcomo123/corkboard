import pytest

from corkboard import create_app, Config

# Fixture to set up the Flask app with SQLite and create necessary tables
@pytest.fixture
def app():
    app = create_app(config_class=Config)

    with app.app_context():
        from corkboard import db
        db.create_all()

    yield app

# Fixture to provide a test client
@pytest.fixture
def client(app):
    return app.test_client()

# Tests for the create_app function

def test_create_app_configurations(app):
    assert app.config['SECRET_KEY'] == '5791628bb0b13ce0c676dfde280ba245'
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///site.db'
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False
    assert app.config['BCRYPT_LOG_ROUNDS'] == 12
    assert app.config['MAIL_SERVER'] == 'smtp.googlemail.com'
    assert app.config['MAIL_PORT'] == 587
    assert app.config['MAIL_USE_TLS'] is True
    assert app.config['MAIL_USERNAME'] == 'richcomo123@gmail.com'
    assert app.config['MAIL_PASSWORD'] == 'ttka qvas cldz ltvg'
    assert app.config['UPLOAD_FOLDER'] == 'static/uploads'


def test_create_app_blueprint_registered(app):
    assert 'main' in app.blueprints

def test_create_app_jinja_filter_added(app):
    assert 'file_type' in app.jinja_env.filters
    assert callable(app.jinja_env.filters['file_type'])





 
