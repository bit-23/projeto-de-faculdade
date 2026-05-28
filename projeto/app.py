import os
from flask import Flask
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

# Configuração do Google OAuth 2.0
app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")
app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET")

# Inicializa o OAuth
oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Importamos o blueprint DEPOIS de configurar o oauth para evitar importação circular
from views import main
app.register_blueprint(main)

# Disponibiliza oauth nas views (para que views.py possa acessar)
import views
views.oauth = oauth

if __name__ == "__main__":
    app.run(debug=True)