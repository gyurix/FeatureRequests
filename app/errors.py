from flask import render_template, Blueprint

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error404(err):
    return render_template("error.html", err=err), 404


@errors.app_errorhandler(429)
def error429(err):
    return "Too many requests (" + err.description + " is the limitation)", 429


@errors.app_errorhandler(500)
def error500(err):
    return render_template("error.html", err=err), 500
