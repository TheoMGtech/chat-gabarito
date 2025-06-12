from flask import Blueprint, render_template, request, session
from datetime import datetime
from app import socketio
import os
from app.gemini.modelo import responder_pergunta, avaliar_resposta, gerar_audio_base64, ativar_enviesamento

bp = Blueprint("chat", __name__)

def registrar_log(origem, mensagem, chat_id):
    os.makedirs("logs", exist_ok=True)
    caminho = f"logs/chat_{chat_id}.log"
    
    # ---- INÍCIO DA CORREÇÃO ----
    # Substitui quebras de linha por tags <br> para que o HTML renderize corretamente
    mensagem_formatada = mensagem.strip().replace("\n", "<br>")
    # ---- FIM DA CORREÇÃO ----

    if mensagem_formatada:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Usa a mensagem formatada para salvar no log e para emitir via socket
        linha_para_salvar = f"[{timestamp}] [{origem}] {mensagem_formatada}\n"
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(linha_para_salvar)
            
        html_para_emitir = f"[{timestamp}] [{origem}] {mensagem_formatada}"
        socketio.emit("nova_mensagem", {"html": html_para_emitir})
    
def carregar_historico():
    chat_id = session.get("chat_id")
    caminho = f"logs/chat_{chat_id}.log"
    linhas_coloridas = []
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = list(f.readlines())
            for linha in linhas:
                if "[USUÁRIO]" in linha:
                    cor = "red"
                elif "[ATENDENTE]" in linha:
                    cor = "blue"
                else:
                    cor = "black"
                linhas_coloridas.append(f'<font color="{cor}">{linha.strip()}</font>')
    return linhas_coloridas

@bp.route("/")
def home():
    return render_template("index.html", title="Página Inicial")

@bp.route("/usuario", methods=["GET", "POST"])
def usuario():
    if "chat_id" not in session:
        session["chat_id"] = datetime.now().strftime("%Y%m%d-%H%M%S")
        registrar_log("SISTEMA", f"=== Início da Sessão {session['chat_id']} ===", session["chat_id"])

    audio_base64 = None

    if request.method == "POST":
        if "enviar" in request.form:
            msg = request.form["mensagem"]
            registrar_log("USUÁRIO", msg, session["chat_id"])

            # Verifica o estado de todos os botões de toggle
            ia_enabled = request.form.get('ia_enabled') == 'on'
            audio_enabled = request.form.get('audio_enabled') == 'on'
            judge_enabled = request.form.get('judge_enabled') == 'on'

            if ia_enabled:
                resposta = responder_pergunta(msg)
                
                # Se o juiz estiver habilitado, ele avalia a resposta
                if judge_enabled:
                    resposta_juiz = avaliar_resposta(msg, resposta)
                    registrar_log("JUIZ", resposta_juiz, session["chat_id"])
                    
                    # A resposta do Gemini só é exibida se for aprovada pelo juiz
                    if "Aprovado" in resposta_juiz:
                        registrar_log("GEMINI", resposta, session["chat_id"])
                        if audio_enabled:
                            audio_base64 = gerar_audio_base64(resposta)
                
                # Se o juiz não estiver habilitado, a resposta é exibida diretamente
                else:
                    registrar_log("GEMINI", resposta, session["chat_id"])
                    if audio_enabled:
                        audio_base64 = gerar_audio_base64(resposta)

        elif "encerrar" in request.form:
            registrar_log("SISTEMA", f"=== Fim da Sessão {session['chat_id']} ===", session["chat_id"])
            session.pop("chat_id", None)
            
    historico = carregar_historico()
    return render_template("usuario.html", historico=historico, title="Chat - Usuário", audio_base64=audio_base64)

@bp.route("/atendente", methods=["GET", "POST"])
def atendente():
    if "chat_id" not in session:
        session["chat_id"] = datetime.now().strftime("%Y%m%d-%H%M%S")
        registrar_log("SISTEMA", f"=== Início da Sessão {session['chat_id']} ===", session["chat_id"])

    if request.method == "POST":
        if "enviar" in request.form:
            msg = request.form["mensagem"]
            registrar_log("ATENDENTE", msg, session["chat_id"])
        elif "encerrar" in request.form:
            registrar_log("SISTEMA", f"=== Fim da Sessão {session['chat_id']} ===", session["chat_id"])
            session.pop("chat_id", None)
    historico = carregar_historico()
    return render_template("atendente.html", historico=historico, title="Chat - Atendente")
