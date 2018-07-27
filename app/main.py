from flask import Flask

from app.api import api, limiter, csrf
from app.config import Config
from app.errors import errors
from app.forms import recaptcha
from app.models import db
from app.pages import pages
from app.utils import get_fields, get_attribute, none_to_empty, entries_to_dict_json


def create_app(testing=False):
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['RECAPTCHA_SITE_KEY'] = Config.CAPTCHA_KEY
    app.config['RECAPTCHA_SECRET_KEY'] = Config.CAPTCHA_SECRET
    app.config['RECAPTCHA_ENABLED'] = Config.CAPTCHA_ENABLED
    if testing:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['RECAPTCHA_ENABLED'] = False

    app.secret_key = Config.SECRET_KEY
    initComponents(app)
    registerPages(app)
    return app


def initComponents(app):
    db.init_app(app)
    recaptcha.init_app(app)
    limiter.init_app(app)
    if app.config['TESTING']:
        limiter.enabled = False
    csrf.init_app(app)


def registerPages(app):
    app.register_blueprint(api)
    app.register_blueprint(pages)
    app.register_blueprint(errors)

    @app.context_processor
    def processors():
        return dict(get_fields=get_fields,
                    get_attribute=get_attribute,
                    none_to_empty=none_to_empty,
                    entries_to_dict=entries_to_dict_json,
                    isinstance=isinstance)


def remove_tables(app):
    with app.app_context():
        db.drop_all()


def create_tables(app):
    with app.app_context():
        db.create_all()


def setupTables(app):
    if Config.RESET_TABLES:
        remove_tables(app)
    create_tables(app)


def runApp(app):
    app.run(host=Config.HOST, port=Config.PORT)


app = create_app()
setupTables(app)

if __name__ == '__main__':
    runApp(app)
