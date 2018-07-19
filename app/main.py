from flask import Flask

from app.api import api, limiter, csrf
from app.config import Config
from app.errors import errors
from app.forms import recaptcha
from app.models import db
from app.pages import pages

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RECAPTCHA_SITE_KEY'] = Config.CAPTCHA_KEY
app.config['RECAPTCHA_SECRET_KEY'] = Config.CAPTCHA_SECRET
app.config['RECAPTCHA_ENABLED'] = Config.CAPTCHA_ENABLED
app.secret_key = Config.SECRET_KEY

db.init_app(app)
db.create_all(app=app)
recaptcha.init_app(app)
limiter.init_app(app)
csrf.init_app(app)

app.register_blueprint(api)
app.register_blueprint(pages)
app.register_blueprint(errors)

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT)
