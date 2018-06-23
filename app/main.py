from flask import Flask

from api import api
from app.config import Config
from errors import errors
from models import db
from pages import pages

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = Config.SECRET_KEY

app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(pages)
app.register_blueprint(errors)

db.init_app(app)

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT)
