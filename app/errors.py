from flask import render_template, Blueprint, request

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(403)
def error403(err):
    if request.path.startswith("/api/"):
        return "The used form is invalid, please refresh the page"
    err.description = "The used form is invalid, please refresh the page"
    return render_template("error.html", err=err), 403


@errors.app_errorhandler(404)
def error404(err):
    if request.path.startswith("/api/"):
        return "Invalid API method - " + request.path[5:], 404
    return render_template("error.html", err=err), 404


@errors.app_errorhandler(429)
def error429(err):
    return "Too many requests (" + err.description + " is the limitation)", 429


@errors.app_errorhandler(500)
def error500(err):
    return render_template("error.html", err=err), 500
