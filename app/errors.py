from flask import render_template, Blueprint

errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def error404():
    return render_template("error.html"), 404


@errors.errorhandler(500)
def error500():
    return render_template("error.html"), 500
