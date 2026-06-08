import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector


main = Blueprint("main", __name__)

# oauth — injetado pelo app.py
oauth = None

#---------------------------------------------------------------------------
# CAMINHO PRA GUARDA FOTOS DE PERFEILS
#---------------------------------------------------------------------------
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# =====================================================
# CONEXÃO MYSQL
# =====================================================
def conectar():
    return mysql.connector.connect(
        host="100.120.87.102",
        port=3306,
        database="ServiceConnect",
        user="root",
        password="h8x1e0k7"
    )


# =====================================================
# PRE HOME PUBLICA
# =====================================================
@main.route("/")
def preHome():
    return render_template("exercicios.html")

# =====================================================
# HOME PUBLICA
# =====================================================
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
            "SELECT * FROM usuarios WHERE idUsuarios = %s",
            (session["user_id"],)
        )
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

    except Exception as e:
        print(e)

    return render_template("home.html", usuario=usuario)


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

    nome  = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    cpf   = request.form.get("cpf", "").strip()
    senha = request.form.get("senha")

    if not nome or not email or not cpf or not senha:
        return render_template("cadastro.html", erro="Preencha todos os campos.")

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
            return render_template("cadastro.html", erro="Email ou CPF já cadastrado.")

        cursor.execute(
            "INSERT INTO usuarios (nome, email, cpf, senha) VALUES (%s, %s, %s, %s)",
            (nome, email, cpf, senha)
        )
        conn.commit()
        session["user_id"] = cursor.lastrowid
        session["user_nome"] = nome

    except Exception as e:
        return f"Erro ao cadastrar: {e}"

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return redirect(url_for("main.pagina_home"))


# =====================================================
# CATEGORIA
# =====================================================
@main.route("/categoria")
def categoria():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM usuarios WHERE idUsuarios = %s",
        (session["user_id"],)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("categoria.html", usuario=usuario)


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

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM usuarios WHERE idUsuarios = %s",
        (session["user_id"],)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("Comofunciona.html", usuario=usuario)


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

    nome  = user_info.get("name", "")
    email = user_info.get("email", "")

    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
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
        if cursor: cursor.close()
        if conn: conn.close()

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
        "SELECT idUsuarios, nome, email, cpf, foto FROM usuarios WHERE idUsuarios = %s",
        (session["user_id"],)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("perfil.html", usuario=usuario)


# =====================================================
# ATUALIZAR FOTO DO USUARIO
# =====================================================
@main.route("/atualizar_foto", methods=["POST"])
def atualizar_foto():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    foto = request.files.get("foto")

    if not foto or not allowed_file(foto.filename):
        return redirect(url_for("main.perfil"))

    filename = secure_filename(f"{session['user_id']}_{foto.filename}")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    foto.save(os.path.join(UPLOAD_FOLDER, filename))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET foto = %s WHERE idUsuarios = %s",
        (filename, session["user_id"])
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("main.perfil"))


# =====================================================
# BUSCAR SERVIÇOS
# =====================================================
@main.route("/buscar")
def buscar_servicos():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE idUsuarios = %s",
        (session["user_id"],)
    )
    usuario = cursor.fetchone()

    cursor.execute(
        """
        SELECT s.*, c.nome AS categoria_nome,
               u.nome AS cliente_nome,
               u.foto AS cliente_foto
        FROM servicos s
        LEFT JOIN categorias c ON s.categoria_id = c.id
        LEFT JOIN usuarios u ON s.cliente_id = u.idUsuarios
        WHERE s.status = 'aberto'
        ORDER BY s.data_criacao DESC
        """
    )
    servicos = cursor.fetchall()
    cursor.close()
    conn.close()

    categoria_selecionada = request.args.get("categoria", "todos")

    return render_template("buscar.html", usuario=usuario, servicos=servicos, categoria_selecionada=categoria_selecionada)


# =====================================================
# PROVER SERVIÇOS
# =====================================================
@main.route("/prover")
def procura_servicos():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE idUsuarios = %s",
        (session["user_id"],)
    )
    usuario = cursor.fetchone()

    cursor.execute(
        """
        SELECT s.*, c.nome AS categoria_nome
        FROM servicos s
        LEFT JOIN categorias c ON s.categoria_id = c.id
        WHERE s.cliente_id = %s
        ORDER BY s.data_criacao DESC
        """,
        (session["user_id"],)
    )
    servicos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("prover.html", usuario=usuario, servicos=servicos)


# =====================================================
# PUBLICAR SERVIÇO
# =====================================================
@main.route("/publicar_servico", methods=["POST"])
def publicar_servico():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    titulo       = request.form.get("titulo")
    categoria_id = request.form.get("categoria_id")
    valor_min    = request.form.get("valor_min") or None
    valor_max    = request.form.get("valor_max") or None
    prazo_dias   = request.form.get("prazo_dias") or None
    descricao    = request.form.get("descricao")

    foto = request.files.get("foto_servico")
    filename = None

    if foto and allowed_file(foto.filename):
        filename = secure_filename(f"servico_{session['user_id']}_{foto.filename}")
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        foto.save(os.path.join(UPLOAD_FOLDER, filename))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO servicos
        (cliente_id, categoria_id, titulo, descricao, valor_min, valor_max, prazo_dias, foto)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (session["user_id"], categoria_id, titulo, descricao, valor_min, valor_max, prazo_dias, filename)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("main.procura_servicos"))


# =====================================================
# EXCLUIR SERVIÇO
# =====================================================
@main.route("/excluir_servico/<int:servico_id>", methods=["POST"])
def excluir_servico(servico_id):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM servicos WHERE id = %s AND cliente_id = %s",
        (servico_id, session["user_id"])
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("main.procura_servicos"))


# =====================================================
# ENVIAR PROPOSTA
# =====================================================
@main.route("/enviar_proposta/<int:servico_id>", methods=["POST"])
def enviar_proposta(servico_id):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    mensagem   = request.form.get("mensagem")
    valor      = request.form.get("valor") or None
    prazo_dias = request.form.get("prazo_dias") or None

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO propostas
        (servico_id, prestador_id, mensagem, valor, prazo_dias)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (servico_id, session["user_id"], mensagem, valor, prazo_dias)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("main.buscar_servicos"))


# =====================================================
# VER PROPOSTAS DO SERVIÇO
# =====================================================
@main.route("/servico/<int:servico_id>/propostas")
def ver_propostas(servico_id):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE idUsuarios = %s",
        (session["user_id"],)
    )
    usuario = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM servicos WHERE id = %s AND cliente_id = %s",
        (servico_id, session["user_id"])
    )
    servico = cursor.fetchone()

    if not servico:
        return redirect(url_for("main.procura_servicos"))

    cursor.execute(
        """
        SELECT p.*, u.nome AS prestador_nome, u.foto AS prestador_foto
        FROM propostas p
        LEFT JOIN usuarios u ON p.prestador_id = u.idUsuarios
        WHERE p.servico_id = %s
        ORDER BY p.data_envio DESC
        """,
        (servico_id,)
    )
    propostas = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("propostas.html", usuario=usuario, servico=servico, propostas=propostas)


# =====================================================
# ACEITAR / RECUSAR PROPOSTA
# =====================================================
@main.route("/proposta/<int:proposta_id>/<acao>", methods=["POST"])
def responder_proposta(proposta_id, acao):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    if acao not in ("aceita", "recusada"):
        return redirect(url_for("main.procura_servicos"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "UPDATE propostas SET status = %s WHERE id = %s",
        (acao, proposta_id)
    )

    if acao == "aceita":
        cursor.execute("SELECT * FROM propostas WHERE id = %s", (proposta_id,))
        proposta = cursor.fetchone()

        cursor.execute("SELECT * FROM servicos WHERE id = %s", (proposta["servico_id"],))
        servico = cursor.fetchone()

        cursor.execute("SELECT id FROM contratos WHERE proposta_id = %s", (proposta_id,))
        existente = cursor.fetchone()

        if not existente:
            cursor.execute(
                """
                INSERT INTO contratos
                (servico_id, proposta_id, cliente_id, prestador_id, valor_final)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    proposta["servico_id"],
                    proposta_id,
                    servico["cliente_id"],
                    proposta["prestador_id"],
                    proposta["valor"]
                )
            )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(request.referrer or url_for("main.procura_servicos"))

# =====================================================
# MINHAS PROPOSTAS (PRESTADOR)
# =====================================================
@main.route("/minhas_propostas")
def minhas_propostas():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE idUsuarios = %s",
        (session["user_id"],)
    )
    usuario = cursor.fetchone()

    cursor.execute(
        """
        SELECT p.*,
               s.titulo AS servico_titulo,
               s.descricao AS servico_descricao,
               u.nome AS cliente_nome,
               u.foto AS cliente_foto,
               c.id AS contrato_id
        FROM propostas p
        LEFT JOIN servicos s ON p.servico_id = s.id
        LEFT JOIN usuarios u ON s.cliente_id = u.idUsuarios
        LEFT JOIN contratos c ON c.proposta_id = p.id
        WHERE p.prestador_id = %s
        ORDER BY p.data_envio DESC
        """,
        (session["user_id"],)
    )
    propostas = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("minhas_propostas.html", usuario=usuario, propostas=propostas)


# =====================================================
# MEUS CONTRATOS
# =====================================================
@main.route("/meus_contratos")
def meus_contratos():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE idUsuarios = %s",
        (session["user_id"],)
    )
    usuario = cursor.fetchone()

    cursor.execute(
        """
        SELECT c.*, s.titulo AS servico_titulo,
               uc.nome AS cliente_nome,
               up.nome AS prestador_nome
        FROM contratos c
        LEFT JOIN servicos s ON c.servico_id = s.id
        LEFT JOIN usuarios uc ON c.cliente_id = uc.idUsuarios
        LEFT JOIN usuarios up ON c.prestador_id = up.idUsuarios
        WHERE c.cliente_id = %s OR c.prestador_id = %s
        ORDER BY c.data_inicio DESC
        """,
        (session["user_id"], session["user_id"])
    )
    contratos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("meus_contratos.html", usuario=usuario, contratos=contratos)


# =====================================================
# VER CONTRATO
# =====================================================
@main.route("/contrato/<int:contrato_id>")
def ver_contrato(contrato_id):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE idUsuarios = %s",
        (session["user_id"],)
    )
    usuario = cursor.fetchone()

    cursor.execute(
        """
        SELECT c.*,
               s.titulo AS servico_titulo,
               s.descricao AS servico_descricao,
               p.mensagem AS proposta_mensagem,
               p.prazo_dias AS proposta_prazo,
               uc.nome AS cliente_nome,
               uc.foto AS cliente_foto,
               up.nome AS prestador_nome,
               up.foto AS prestador_foto
        FROM contratos c
        LEFT JOIN servicos s ON c.servico_id = s.id
        LEFT JOIN propostas p ON c.proposta_id = p.id
        LEFT JOIN usuarios uc ON c.cliente_id = uc.idUsuarios
        LEFT JOIN usuarios up ON c.prestador_id = up.idUsuarios
        WHERE c.id = %s
        AND (c.cliente_id = %s OR c.prestador_id = %s)
        """,
        (contrato_id, session["user_id"], session["user_id"])
    )
    contrato = cursor.fetchone()
    cursor.close()
    conn.close()

    if not contrato:
        return redirect(url_for("main.pagina_home"))

    return render_template("contrato.html", usuario=usuario, contrato=contrato)


# =====================================================
# ASSINAR CONTRATO
# =====================================================
@main.route("/contrato/<int:contrato_id>/assinar", methods=["POST"])
def assinar_contrato(contrato_id):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM contratos WHERE id = %s", (contrato_id,))
    contrato = cursor.fetchone()

    if not contrato:
        cursor.close()
        conn.close()
        return redirect(url_for("main.pagina_home"))

    if session["user_id"] == contrato["cliente_id"]:
        cursor.execute(
            "UPDATE contratos SET assinatura_cliente = 1 WHERE id = %s",
            (contrato_id,)
        )
    elif session["user_id"] == contrato["prestador_id"]:
        cursor.execute(
            "UPDATE contratos SET assinatura_prestador = 1 WHERE id = %s",
            (contrato_id,)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("main.ver_contrato", contrato_id=contrato_id))


# =====================================================
# LOGOUT
# =====================================================
@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))