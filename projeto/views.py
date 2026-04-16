
from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector

main = Blueprint("main", __name__)

# oauth — injetado pelo app.py
oauth = None

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

@main.route("/cadastro", methods=["POST"])
def cadastro_post():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    cpf = request.form.get("CPF", "").strip()
    senha = request.form.get("senha")

    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="faculdade",
            user="root",
            password="h8x1e0k7",
        )
        cursor = conn.cursor(dictionary=True)

        # Verifica se email ou CPF já existem
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s OR cpf = %s",
            (email, cpf),
        )
        existente = cursor.fetchone()

        if existente:
            if existente.get("email") == email:
                cursor.close()
                conn.close()
                return render_template(
                    "cadastro.html",
                    erro="Este email já está cadastrado.",
                )

            if existente.get("cpf") == cpf:
                cursor.close()
                conn.close()
                return render_template(
                    "cadastro.html",
                    erro="Este CPF já está cadastrado.",
                )

        cursor.execute(
            "INSERT INTO usuarios (nome, email, cpf, senha) VALUES (%s, %s, %s, %s)",
            (nome, email, cpf, senha),
        )
        conn.commit()
        session["user_id"] = cursor.lastrowid
        session["user_nome"] = nome

        cursor.close()
        conn.close()

    except Exception as e:
        print("Erro ao cadastrar:", e)
        return render_template("cadastro.html", erro="Erro ao criar conta. Tente novamente.")

    return redirect(url_for("main.home"))

@main.route("/categoria")
def categoria():
    return render_template("categoria.html")

@main.route("/Categoria", methods=["POST"])
def salvar_categoria():
    categoria = request.form.get("categoria")
    session["categoria"] = categoria
    return redirect(url_for("main.home"))

@main.route("/ComoFunciona")
def ComoFunciona():
    return render_template("Comofunciona.html")

# ===== Google OAuth 2.0 =====

@main.route("/login/google")
def google_login():
    redirect_uri = url_for("main.google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@main.route("/login/google/callback")# APi de verificação 
def google_callback():
    try:
        token = oauth.google.authorize_access_token()
    except Exception:
        return redirect(url_for("main.login"))

    if not token:
        return redirect(url_for("main.login"))

    # Extrair dados do usuário
    user_info = token.get("userinfo")
    nome = user_info.get("name", "")
    email = user_info.get("email", "")

    # Buscar ou criar usuário no banco
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="faculdade",
            user="root",
            password="h8x1e0k7",
        )
        cursor = conn.cursor(dictionary=True)

        # Verifica se já existe
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            # Cria novo usuário via Google
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, "google"),
            )
            conn.commit()
            session["user_id"] = cursor.lastrowid
            session["user_nome"] = nome
        else:
            session["user_id"] = usuario.get("id")
            session["user_nome"] = usuario.get("nome")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Erro no banco durante Google Login:", e)
        return redirect(url_for("main.login"))

    return redirect(url_for("main.home"))