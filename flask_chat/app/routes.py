from flask import Blueprint, render_template, request, session, jsonify, url_for, current_app
from datetime import datetime
from app import socketio
import os
import traceback
from werkzeug.utils import secure_filename
from app.gemini.modelo import responder_pergunta, avaliar_resposta, gerar_audio_base64

bp = Blueprint("chat", __name__)

def salvar_arquivo(arquivo):
    if not arquivo or arquivo.filename == '':
        return None, None
    
    filename = secure_filename(arquivo.filename)
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    caminho_local = os.path.join(upload_folder, filename)
    arquivo.save(caminho_local)
    
    url_web = url_for('static', filename=f'uploads/{filename}')
    return url_web, caminho_local

def registrar_log(origem, mensagem, chat_id, urls_imagens=None):
    os.makedirs("logs", exist_ok=True)
    caminho = f"logs/chat_{chat_id}.log"
    
    mensagem_final = mensagem.strip().replace("\n", "<br>")
    
    if urls_imagens:
        tags_imagem = "".join([f"[IMAGEM:{url}]" for url in urls_imagens])
        mensagem_final = f"{tags_imagem}<br>{mensagem_final}"

    if mensagem_final or urls_imagens:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha_para_salvar = f"[{timestamp}] [{origem}] {mensagem_final}\n"
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(linha_para_salvar)
        
        html_para_emitir = f"[{timestamp}] [{origem}] {mensagem_final}"
        socketio.emit("nova_mensagem", {"html": html_para_emitir})

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
        session["chat_id"] = datetime.now().strftime("%Y%m%d-%H%M%S")
        registrar_log("SISTEMA", f"=== Início da Sessão {session['chat_id']} ===", session["chat_id"])
    historico = carregar_historico()
    return render_template("atendente.html", 
                           historico=historico, 
                           title="Chat - Atendente",
                           role="atendente",
                           post_url=url_for('chat.send_attendant_message'))

def carregar_historico():
    chat_id = session.get("chat_id")
    if not chat_id: return []
    caminho = f"logs/chat_{chat_id}.log"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f.readlines()]
    return []

@bp.route("/send_message", methods=["POST"])
def send_message():
    try:
        msg = request.form.get("mensagem", "")
        imagens = request.files.getlist('imagens')
        chat_id = session.get("chat_id")

        if not chat_id: return jsonify({"status": "error", "message": "Sessão não encontrada"}), 400
        if not msg.strip() and not imagens: return jsonify({"status": "error", "message": "Mensagem ou imagem vazia"}), 400

        saved_files = [salvar_arquivo(img) for img in imagens if img]
        urls_imagens = [item[0] for item in saved_files]
        caminhos_locais = [item[1] for item in saved_files]
        
        registrar_log("USUÁRIO", msg, chat_id, urls_imagens)

        ia_enabled = request.form.get('ia_enabled') == 'on'
        audio_enabled = request.form.get('audio_enabled') == 'on'
        judge_enabled = request.form.get('judge_enabled') == 'on'
        audio_base64 = None

        if ia_enabled:
            resposta = responder_pergunta(msg, caminhos_locais)
            
            if judge_enabled:
                resposta_juiz = avaliar_resposta(msg, resposta)
                registrar_log("JUIZ", resposta_juiz, chat_id)
                if "Aprovado" in resposta_juiz:
                    registrar_log("GEMINI", resposta, chat_id)
                    if audio_enabled: audio_base64 = gerar_audio_base64(resposta)
            else:
                registrar_log("GEMINI", resposta, chat_id)
                if audio_enabled: audio_base64 = gerar_audio_base64(resposta)

        return jsonify({"status": "success", "audio_base64": audio_base64})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route("/send_attendant_message", methods=["POST"])
def send_attendant_message():
    try:
        msg = request.form.get("mensagem", "")
        imagens = request.files.getlist('imagens')
        chat_id = session.get("chat_id")

        if not chat_id: return jsonify({"status": "error", "message": "Sessão não encontrada"}), 400
        if not msg.strip() and not imagens: return jsonify({"status": "error", "message": "Mensagem ou imagem vazia"}), 400
            
        saved_files = [salvar_arquivo(img) for img in imagens if img]
        urls_imagens = [item[0] for item in saved_files]

        registrar_log("ATENDENTE", msg, chat_id, urls_imagens)
        return jsonify({"status": "success"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route("/encerrar_sessao")
def encerrar_sessao():
    chat_id = session.get("chat_id")
    if chat_id:
        registrar_log("SISTEMA", f"=== Fim da Sessão {chat_id} ===", chat_id)
        session.pop("chat_id", None)
    return jsonify({"status": "success", "message": "Sessão encerrada."})