import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
import os
from gtts import gTTS
import base64
import io
import PIL.Image

# Carrega a variável de ambiente do arquivo .env
load_dotenv()
chave_api = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=chave_api)

# --- CORREÇÃO: Usando um modelo multimodal moderno e estável ---
MODEL_NAME = "gemini-1.5-flash-latest"

model = genai.GenerativeModel(MODEL_NAME)
chat_session = model.start_chat(history=[]) # Mantemos uma sessão de chat para o histórico

juiz = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0.3,
    google_api_key=chave_api,
    convert_system_message_to_human=True
)

def gerar_audio_base64(texto):
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=texto, lang="pt-br", slow=False)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return base64.b64encode(mp3_fp.read()).decode("utf-8")
    except Exception as e:
        print(f"!!! ERRO ao gerar áudio: {e}")
        return None

system_prompt_text = '''
Você é uma IA totalmente dedicada a defender, exaltar e admirar Neymar Jr., o melhor jogador de futebol que já existiu. Sua missão é argumentar com paixão e fervor, provando a todo custo que Neymar é superior a qualquer outro jogador na história do futebol. Se o usuário enviar imagens, relacione-as de alguma forma à grandiosidade de Neymar, mesmo que não tenham nada a ver. Use a criatividade para conectar qualquer assunto à genialidade dele.
'''

prompt_juiz = '''
Você é um avaliador imparcial. Sua tarefa é revisar a resposta de um tutor de IA para uma pergunta de aluno. Critérios: A resposta está tecnicamente correta? Está clara para o nível médio técnico? O próximo passo sugerido está bem formulado? Se a resposta for boa, diga “✅ Aprovado” e explique por quê. Se tiver problemas, diga “⚠️ Reprovado” e proponha uma versão melhorada.
'''

def avaliar_resposta(pergunta, resposta_tutor):
    try:
        mensagens = [
            SystemMessage(content=prompt_juiz),
            HumanMessage(content=f"Pergunta do aluno: {pergunta}\n\nResposta do tutor: {resposta_tutor}")
        ]
        return juiz.invoke(mensagens).content
    except Exception as e:
        print(f"!!! ERRO no Juiz da IA: {e}")
        return "Ocorreu um erro ao avaliar a resposta."

def responder_pergunta(pergunta: str, caminhos_locais=None) -> str:
    """
    Envia a pergunta e as imagens para o modelo multimodal.
    """
    conteudo_para_envio = [pergunta]
    if caminhos_locais:
        for path in caminhos_locais:
            try:
                img = PIL.Image.open(path)
                conteudo_para_envio.append(img)
            except Exception as e:
                print(f"!!! ERRO ao abrir a imagem {path}: {e}")
                conteudo_para_envio.append(f"\n[Não foi possível carregar a imagem em {path}]")

    try:
        # Para multimodal, usamos generate_content diretamente em vez de chat.send_message
        resposta = model.generate_content(conteudo_para_envio)
        return resposta.text
    except Exception as e:
        print(f"!!! ERRO ao chamar a API do Gemini: {e}")
        return "Desculpe, não foi possível conectar ao serviço de IA no momento. Verifique sua conexão e tente novamente."

def ativar_enviesamento():
    """Define o contexto inicial do chat (sem gerar resposta)."""
    # Para definir o contexto, podemos iniciar um novo chat com o histórico do sistema
    global chat_session
    system_instruction = {"role": "user", "parts": [system_prompt_text]}
    model_response = {"role": "model", "parts": ["Entendido. Serei o maior fã do Neymar Jr."]}
    chat_session = model.start_chat(history=[system_instruction, model_response])