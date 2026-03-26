
from flask import Blueprint, render_template, request

main = Blueprint("main", __name__)

@main.route("/")
@main.route('/ServiConnect')
def home():
    return render_template("exercicios.html")

@main.route("/home")
def pagina_home():
    return render_template("home.html")

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@main.route("/categoria")
def categoria():
    return render_template("categoria.html")

@main.route("/ComoFunciona")
def ComoFunciona():
    return render_template("Comofunciona.html")