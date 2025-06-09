import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.schema import HumanMessage, SystemMessage
import os
from gtts import gTTS
import base64

def gerar_audio_base64(texto):
    from gtts import gTTS
    import io

    # Gera o áudio em memória (sem salvar no disco)
    mp3_fp = io.BytesIO()
    tts = gTTS(text=texto, lang="pt-br", slow=False)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Converte para base64
    audio_base64 = base64.b64encode(mp3_fp.read()).decode("utf-8")
    return audio_base64




# Carrega a variável de ambiente do arquivo .env (se você estiver usando .env)
load_dotenv()

# Configura a API key
chave_api = os.getenv("GEMINI_API_KEY")

genai.configure(api_key = chave_api)

chat = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=chave_api,
    convert_system_message_to_human=True
)

juiz = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    google_api_key=chave_api,
    convert_system_message_to_human=True
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

system_prompt_text = '''
Você é um tutor de Inteligência Artificial amigável e experiente.
Explique conceitos de forma clara e concisa, adapte-se ao nível do aluno
e sempre ofereça o próximo passo lógico no aprendizado.
'''

prompt_juiz = '''
Você é um avaliador imparcial. Sua tarefa é revisar a resposta de um tutor de IA para uma pergunta de aluno.

Critérios:
- A resposta está técnicamente correta?
- Está clara para o nível médio técnico?
- O próximo passo sugerido está bem formulado?

Se a resposta for boa, diga “✅ Aprovado” e explique por quê.
Se tiver problemas, diga “⚠️ Reprovado” e proponha uma versão melhorada.
'''

agent = initialize_agent(
    llm=chat,
    tools=[],
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    agent_kwargs={
        "prefix": system_prompt_text
    }
)

# rotina para avaliar a resposta do tutor
def avaliar_resposta(pergunta, resposta_tutor):
    mensagens = [
        SystemMessage(content=prompt_juiz),
        HumanMessage(content=f"Pergunta do aluno: {pergunta}\n\nResposta do tutor: {resposta_tutor}")
    ]
    return juiz.invoke(mensagens).content

# rotina para enviar pergunta ao modelo
def responder_pergunta(pergunta: str) -> str:
    resposta = agent.run(pergunta)
    return resposta
