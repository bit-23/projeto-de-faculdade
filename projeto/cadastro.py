from flask import Flask, request, redirect, render_template
import mysql.connector
import bcrypt

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="faculdade"
)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        cursor = db.cursor()

        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return "Email já cadastrado!"

        senha_hash = bcrypt.hashpw(
            senha.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
            (nome, email, senha_hash)
        )

        db.commit()

        return redirect("/login")

    return render_template("cadastro.html")


if __name__ == "__main__":
    app.run(debug=True)
