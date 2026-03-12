import os
import json
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "chave_super_secreta"

ARQUIVO_JSON = "ocorrencias.json"
ARQUIVO_USUARIOS = "usuarios.json"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# =========================
# FUNÇÕES AUXILIARES
# =========================

def carregar_ocorrencias():

    if not os.path.exists(ARQUIVO_JSON):
        return []

    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def salvar_ocorrencias(dados):

    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def gerar_novo_id(dados):

    if not dados:
        return "1"

    ultimo_id = max(int(o["id"]) for o in dados)
    return str(ultimo_id + 1)


def carregar_usuarios():

    if not os.path.exists(ARQUIVO_USUARIOS):
        return []

    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# =========================
# ROTAS PRINCIPAIS
# =========================

@app.route("/")
def index():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("home.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        senha = request.form.get("senha")

        usuarios = carregar_usuarios()

        for u in usuarios:
            if u["email"] == email and u["senha"] == senha:

                session["usuario"] = u["nome"]
                session["email"] = u["email"]

                return redirect(url_for("abrir_ocorrencia"))

        return "Email ou senha inválidos"

    return render_template("login.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("login"))


# =========================
# CADASTRO
# =========================

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")

    usuarios = carregar_usuarios()

    for u in usuarios:
        if u["email"] == email:
            return "Este email já está cadastrado"

    novo_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha
    }

    usuarios.append(novo_usuario)

    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4)

    return redirect(url_for("login"))


# =========================
# ABRIR OCORRÊNCIA
# =========================

@app.route("/abrir", methods=["GET", "POST"])
def abrir_ocorrencia():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        dados = carregar_ocorrencias()
        novo_id = gerar_novo_id(dados)

        setor = request.form.get("setor")
        descricao = request.form.get("descricao")

        foto = request.files.get("foto")

        caminho_foto = ""

        if foto and foto.filename != "":
            nome_arquivo = f"{novo_id}_{foto.filename}"
            caminho_foto = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo)
            foto.save(caminho_foto)

        nova_ocorrencia = {
            "id": novo_id,
            "setor": setor,
            "operador": session["usuario"],
            "email": session["email"],
            "descricao": descricao,
            "foto": caminho_foto,
            "status": "Aberto",
            "tecnico": "",
            "acao": ""
        }

        dados.append(nova_ocorrencia)
        salvar_ocorrencias(dados)

        enviar_email_nova_ocorrencia(nova_ocorrencia)

        return redirect(url_for("consultar_por_id", id=novo_id))

    return render_template("operador.html")

# =========================
# EMAIL PARA COORDENADOR
# =========================

def enviar_email_nova_ocorrencia(ocorrencia):

    email_remetente = "igorsalesleallima@gmail.com"
    senha_app = "vdkhzrxhqppzgxvj"

    # EMAIL DO COORDENADOR (VOCÊ)
    email_destino = "igorsalesleallima@gmail.com"

    mensagem = f"""
Nova ocorrência registrada no sistema

ID: {ocorrencia['id']}
Setor: {ocorrencia['setor']}

Operador: {ocorrencia['operador']}
Email: {ocorrencia['email']}

Descrição:
{ocorrencia['descricao']}

Status: {ocorrencia['status']}
"""

    msg = MIMEText(mensagem)

    msg["Subject"] = f"Nova Ocorrência #{ocorrencia['id']}"
    msg["From"] = email_remetente
    msg["To"] = email_destino

    try:

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()

        servidor.login(email_remetente, senha_app)

        servidor.sendmail(
            email_remetente,
            email_destino,
            msg.as_string()
        )

        servidor.quit()

        print("Email enviado para coordenador")

    except Exception as erro:

        print("Erro ao enviar email:", erro)
        
# =========================
# EMAIL PARA USUÁRIO
# =========================

def enviar_email_usuario(ocorrencia):

    email_remetente = "igorsalesleallima@gmail.com"
    senha_app = "vdkhzrxhqppzgxvj"

    email_destino = ocorrencia["email"]

    mensagem = f"""
Sua ocorrência foi resolvida

ID: {ocorrencia['id']}
Setor: {ocorrencia['setor']}

Técnico: {ocorrencia['tecnico']}

Ação realizada:
{ocorrencia['acao']}

Status: {ocorrencia['status']}
"""

    msg = MIMEText(mensagem)

    msg["Subject"] = f"Ocorrência Resolvida #{ocorrencia['id']}"
    msg["From"] = email_remetente
    msg["To"] = email_destino

    try:

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()

        servidor.login(email_remetente, senha_app)

        servidor.sendmail(
            email_remetente,
            email_destino,
            msg.as_string()
        )

        servidor.quit()

        print("Email enviado para usuário")

    except Exception as erro:

        print("Erro ao enviar email:", erro)


# =========================
# GERIR OCORRÊNCIA
# =========================

@app.route("/gerir", methods=["GET", "POST"])
def gerir_ocorrencia():

    ocorrencia = None
    dados = carregar_ocorrencias()

    if request.method == "POST":

        id_busca = request.form.get("id")

        for o in dados:

            if o["id"] == id_busca:

                ocorrencia = o

                if o["status"] == "Aberto":

                    tecnico = request.form.get("tecnico")
                    acao = request.form.get("acao")

                    if tecnico and acao:

                        o["tecnico"] = tecnico.strip()
                        o["acao"] = acao.strip()
                        o["status"] = "Fechado"

                        salvar_ocorrencias(dados)
                        
                        enviar_email_usuario(o)


                break

    return render_template("coordenador.html", ocorrencia=ocorrencia)


# =========================
# CONSULTA
# =========================

@app.route("/consultar", methods=["GET", "POST"])
def consultar_ocorrencia():

    ocorrencia = None

    if request.method == "POST":

        id_busca = request.form.get("id")
        dados = carregar_ocorrencias()

        for o in dados:

            if o["id"] == id_busca:
                ocorrencia = o
                break

    return render_template("consulta.html", ocorrencia=ocorrencia)


@app.route("/consultar/<id>")
def consultar_por_id(id):

    dados = carregar_ocorrencias()

    for o in dados:

        if o["id"] == id:
            return render_template("consulta.html", ocorrencia=o)

    return "Ocorrência não encontrada"


# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    app.run(debug=True)