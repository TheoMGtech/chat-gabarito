from flask import Blueprint, render_template, request, session, jsonify, url_for
from datetime import datetime
from app import socketio
import os
from app.gemini.modelo import responder_pergunta, avaliar_resposta, gerar_audio_base64

bp = Blueprint("chat", __name__)

def registrar_log(origem, mensagem, chat_id):
    os.makedirs("logs", exist_ok=True)
    caminho = f"logs/chat_{chat_id}.log"
    mensagem_formatada = mensagem.strip().replace("\n", "<br>")
    if mensagem_formatada:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha_para_salvar = f"[{timestamp}] [{origem}] {mensagem_formatada}\n"
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(linha_para_salvar)
        html_para_emitir = f"[{timestamp}] [{origem}] {mensagem_formatada}"
        socketio.emit("nova_mensagem", {"html": html_para_emitir})

def carregar_historico():
    chat_id = session.get("chat_id")
    if not chat_id:
        return []
    caminho = f"logs/chat_{chat_id}.log"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f.readlines()]
    return []

@bp.route("/")
def home():
    return render_template("index.html", title="Página Inicial")

@bp.route("/usuario", methods=["GET"])
def usuario():
    if "chat_id" not in session:
        session["chat_id"] = datetime.now().strftime("%Y%m%d-%H%M%S")
        registrar_log("SISTEMA", f"=== Início da Sessão {session['chat_id']} ===", session["chat_id"])
    
    historico = carregar_historico()
    return render_template("usuario.html", 
                           historico=historico, 
                           title="Chat - Usuário",
                           role="usuario",
                           post_url=url_for('chat.send_message'))

@bp.route("/atendente", methods=["GET"])
def atendente():
    if "chat_id" not in session:
        # Se não houver sessão, o atendente não tem a quem atender.
        # Poderíamos redirecionar ou mostrar uma mensagem.
        # Por enquanto, vamos criar uma sessão para demonstração.
        session["chat_id"] = datetime.now().strftime("%Y%m%d-%H%M%S")
        registrar_log("SISTEMA", f"=== Início da Sessão {session['chat_id']} ===", session["chat_id"])

    historico = carregar_historico()
    return render_template("atendente.html", 
                           historico=historico, 
                           title="Chat - Atendente",
                           role="atendente",
                           post_url=url_for('chat.send_attendant_message'))

@bp.route("/send_message", methods=["POST"])
def send_message():
    # Rota para mensagens enviadas pelo USUÁRIO
    msg = request.form.get("mensagem", "")
    if not msg.strip():
        return jsonify({"status": "error", "message": "Mensagem vazia"}), 400

    chat_id = session.get("chat_id")
    if not chat_id:
        return jsonify({"status": "error", "message": "Sessão não encontrada"}), 400

    registrar_log("USUÁRIO", msg, chat_id)

    ia_enabled = request.form.get('ia_enabled') == 'on'
    audio_enabled = request.form.get('audio_enabled') == 'on'
    judge_enabled = request.form.get('judge_enabled') == 'on'
    audio_base64 = None

    if ia_enabled:
        resposta = responder_pergunta(msg)
        if judge_enabled:
            resposta_juiz = avaliar_resposta(msg, resposta)
            registrar_log("JUIZ", resposta_juiz, chat_id)
            if "Aprovado" in resposta_juiz:
                registrar_log("GEMINI", resposta, chat_id)
                if audio_enabled:
                    audio_base64 = gerar_audio_base64(resposta)
        else:
            registrar_log("GEMINI", resposta, chat_id)
            if audio_enabled:
                audio_base64 = gerar_audio_base64(resposta)

    return jsonify({"status": "success", "audio_base64": audio_base64})

@bp.route("/send_attendant_message", methods=["POST"])
def send_attendant_message():
    # Rota para mensagens enviadas pelo ATENDENTE
    msg = request.form.get("mensagem", "")
    if not msg.strip():
        return jsonify({"status": "error", "message": "Mensagem vazia"}), 400
    
    chat_id = session.get("chat_id")
    if not chat_id:
        return jsonify({"status": "error", "message": "Sessão não encontrada"}), 400
        
    registrar_log("ATENDENTE", msg, chat_id)
    return jsonify({"status": "success"})

@bp.route("/encerrar_sessao")
def encerrar_sessao():
    chat_id = session.get("chat_id")
    if chat_id:
        registrar_log("SISTEMA", f"=== Fim da Sessão {chat_id} ===", chat_id)
        session.pop("chat_id", None)
    return jsonify({"status": "success", "message": "Sessão encerrada."})