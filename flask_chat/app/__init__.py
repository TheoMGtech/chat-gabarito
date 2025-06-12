from flask import Flask
from flask_socketio import SocketIO
from app.gemini.modelo import ativar_enviesamento

app = Flask(__name__)
app.secret_key = "supersecretkey"
socketio = SocketIO(app)

from app.routes import bp
app.register_blueprint(bp)

# ativa enviesamento ao iniciar o servidor
with app.app_context():
    ativar_enviesamento()
    print("Enviesamento ativado com sucesso!")