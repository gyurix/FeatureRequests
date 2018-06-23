from flask import Flask

from api import api
from errors import errors
from models import db
from pages import pages

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fr:fr123@localhost/fr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'oXWerTpO!ThZ!uAAENnV5k9F'

app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(pages)
app.register_blueprint(errors)

db.init_app(app)

if __name__ == '__main__':
    app.run()
