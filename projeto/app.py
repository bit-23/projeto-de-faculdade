from flask import Flask
from views import main
from authlib.integrations.flask_client import OAuth
import views
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuração do Google OAuth 2.0
app.config["GOOGLE_CLIENT_ID"] = "987145247771-7p0qifomodu85k32kut9a2h227a5jbv9.apps.googleusercontent.com"
app.config["GOOGLE_CLIENT_SECRET"] = "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"

# Registra o blueprint
app.register_blueprint(main)

# Inicializa o OAuth
oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Disponibiliza oauth nas views
views.oauth = oauth

if __name__ == "__main__":
    app.run(debug=True)
