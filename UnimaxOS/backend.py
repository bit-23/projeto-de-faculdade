import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

ARQUIVO_JSON = "ocorrencias.json"
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/home")
def home():
    return render_template("home.html")

# =========================
# FUNÇÕES AUXILIARES
# =========================

def carregar_ocorrencias():
    if not os.path.exists(ARQUIVO_JSON):
        return []
    with open(ARQUIVO_JSON, "r") as f:
        return json.load(f)


def salvar_ocorrencias(dados):
    with open(ARQUIVO_JSON, "w") as f:
        json.dump(dados, f, indent=4)


def gerar_novo_id(dados):
    if not dados:
        return "1"
    ultimo_id = max(int(o["id"]) for o in dados)
    return str(ultimo_id + 1)


# =========================
# ROTAS
# =========================

@app.route("/")
def index():
    return redirect(url_for("home"))


# -------------------------
# A) MÓDULO OPERADOR
# -------------------------

@app.route("/abrir", methods=["GET", "POST"])
def abrir_ocorrencia():
    if request.method == "POST":

        dados = carregar_ocorrencias()
        novo_id = gerar_novo_id(dados)

        setor = request.form["setor"]
        operador = request.form["operador"]
        descricao = request.form["descricao"]
        foto = request.files["foto"]

        caminho_foto = ""
        if foto:
            nome_arquivo = f"{novo_id}_{foto.filename}"
            caminho_foto = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo)
            foto.save(caminho_foto)

        nova_ocorrencia = {
            "id": novo_id,
            "setor": setor,
            "operador": operador,
            "descricao": descricao,
            "foto": caminho_foto,
            "status": "Aberto",
            "tecnico": "",
            "acao": ""
        }

        dados.append(nova_ocorrencia)
        salvar_ocorrencias(dados)

        return redirect(url_for("consultar_ocorrencia", id=novo_id))

    return render_template("operador.html")


# -------------------------
# B) MÓDULO COORDENADOR
# -------------------------

@app.route("/gerir", methods=["GET", "POST"])
def gerir_ocorrencia():
    ocorrencia = None

    if request.method == "POST":
        id_busca = request.form.get("id")
        dados = carregar_ocorrencias()

        for o in dados:
            if o["id"] == id_busca:
                ocorrencia = o

                # Só permite fechar se estiver Aberto
                if o["status"] == "Aberto":

                    tecnico = request.form.get("tecnico")
                    acao = request.form.get("acao")

                    # Verifica se os campos foram preenchidos
                    if tecnico and acao:
                        o["tecnico"] = tecnico.strip()
                        o["acao"] = acao.strip()
                        o["status"] = "Fechado"
                        salvar_ocorrencias(dados)

                break

    return render_template("coordenador.html", ocorrencia=ocorrencia)


# -------------------------
# C) CONSULTA PÚBLICA
# -------------------------

@app.route("/consultar", methods=["GET", "POST"])
def consultar_ocorrencia():
    ocorrencia = None

    if request.method == "POST":
        id_busca = request.form["id"]
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

if __name__ == "__main__":
    app.run(debug=True)