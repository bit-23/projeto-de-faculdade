
from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector

main = Blueprint("main", __name__)

# oauth — injetado pelo app.py
oauth = None


# =====================================================
# CONEXÃO MYSQL
# =====================================================
def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        database="ServiceConnect",
        user="root",
        password="h8x1e0k7"
    )


# =====================================================
# HOME PUBLICA
# =====================================================
@main.route("/")
@main.route("/ServiConnect")
def home():
    return render_template("exercicios.html")


# =====================================================
# HOME LOGADA
# =====================================================
@main.route("/home")
def pagina_home():

    print(session)

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    usuario = None

    try:
        conn = conectar()

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT * FROM usuarios
            WHERE idUsuarios = %s
            """,
            (session["user_id"],)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

    except Exception as e:
        print(e)

    return render_template(
        "home.html",
        usuario=usuario
    )


# =====================================================
# LOGIN NORMAL
# =====================================================
@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    senha = request.form.get("senha")

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE email=%s AND senha=%s",
        (email, senha)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        session["user_id"] = usuario["idUsuarios"]
        session["user_nome"] = usuario["nome"]

        return redirect(url_for("main.pagina_home"))

    return render_template("login.html", erro="Email ou senha inválidos.")


# =====================================================
# CADASTRO
# =====================================================
@main.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


@main.route("/cadastro", methods=["POST"])
def cadastro_post():

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    cpf = request.form.get("cpf", "").strip()
    senha = request.form.get("senha")

    if not nome or not email or not cpf or not senha:
        return render_template(
            "cadastro.html",
            erro="Preencha todos os campos."
        )

    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email=%s OR cpf=%s",
            (email, cpf)
        )

        existente = cursor.fetchone()

        if existente:
            return render_template(
                "cadastro.html",
                erro="Email ou CPF já cadastrado."
            )

        cursor.execute(
            """
            INSERT INTO usuarios
            (nome, email, cpf, senha)
            VALUES (%s, %s, %s, %s)
            """,
            (nome, email, cpf, senha)
        )

        conn.commit()

        session["user_id"] = cursor.lastrowid
        session["user_nome"] = nome

    except Exception as e:
        return f"Erro ao cadastrar: {e}"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("main.pagina_home"))


# =====================================================
# CATEGORIA
# =====================================================
@main.route("/categoria")
def categoria():
    return render_template("categoria.html")


@main.route("/salvar_categoria", methods=["POST"])
def salvar_categoria():

    categoria = request.form.get("categoria")
    session["categoria"] = categoria

    return redirect(url_for("main.pagina_home"))


# =====================================================
# COMO FUNCIONA
# =====================================================
@main.route("/ComoFunciona")
def ComoFunciona():
    return render_template("Comofunciona.html")


# =====================================================
# LOGIN GOOGLE
# =====================================================
@main.route("/login/google")
def google_login():
    redirect_uri = url_for("main.google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


# =====================================================
# CALLBACK GOOGLE
# =====================================================
@main.route("/login/google/callback")
def google_callback():

    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        print("Erro OAuth:", e)
        return redirect(url_for("main.login"))

    if not token:
        return redirect(url_for("main.login"))

    user_info = token.get("userinfo")

    if not user_info:
        return redirect(url_for("main.login"))

    nome = user_info.get("name", "")
    email = user_info.get("email", "")

    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s",
            (email,)
        )

        usuario = cursor.fetchone()

        # se não existe cria
        if not usuario:

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO usuarios
                (nome, email, senha)
                VALUES (%s, %s, %s)
                """,
                (nome, email, "google")
            )

            conn.commit()

            session["user_id"] = cursor.lastrowid
            session["user_nome"] = nome

        else:
            session["user_id"] = usuario["idUsuarios"]
            session["user_nome"] = usuario["nome"]

    except Exception as e:
        print("Erro banco:", e)
        return redirect(url_for("main.login"))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("main.pagina_home"))


# =====================================================
# PERFIL
# =====================================================
@main.route("/perfil")
def perfil():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT idUsuarios, nome, email, cpf
        FROM usuarios
        WHERE idUsuarios = %s
        """,
        (session["user_id"],)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("perfil.html", usuario=usuario)


# =====================================================
# BUSCAR SERVIÇOS
# =====================================================
@main.route("/buscar")
def buscar_servicos():
    return render_template("buscar.html")


# =====================================================
# PROVER SERVIÇOS
# =====================================================
@main.route("/prover")
def procura_servicos():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor()

    cursor.close()
    conn.close()

    return render_template("prover.html")


# =====================================================
# LOGOUT
# =====================================================
@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))