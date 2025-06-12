# 💬 Chat com Assistente de IA

E aí\! Este é um projeto de chat que desenvolvemos para o 2º ano do nosso curso técnico em Análise de Dados & Desenvolvimento de Sistemas (com foco em Dados e IA's). A aplicação simula uma conversa em tempo real entre um **usuário** e um **atendente**, mas com um toque especial: uma Inteligência Artificial (Google Gemini) que pode entrar na conversa para tirar dúvidas, gerar respostas em áudio e ter suas próprias respostas avaliadas por um "Juiz" de IA.

## 🚀 Teste ao Vivo

Acesse a versão da aplicação publicada no Render:

**[https://chat-gabarito.onrender.com/](https://chat-gabarito.onrender.com/)**

## ✨ Funcionalidades Principais

  * **Chat em Tempo Real**: Comunicação instantânea entre as janelas do usuário e do atendente usando WebSockets.
  * **Assistente com IA**: Ao clicar no botão "Resposta com IA", o usuário pode fazer perguntas que são respondidas pelo modelo Gemini do Google.
  * **Respostas em Áudio**: O usuário pode optar por receber a resposta da IA como uma mensagem de áudio interativa, similar ao WhatsApp.
  * **Juiz de IA**: Um segundo modelo de IA avalia a qualidade e precisão das respostas do assistente principal, aprovando-as ou sugerindo melhorias.
  * **Interface Moderna**: Layout inspirado em aplicativos de mensagem populares, com o histórico de chat sendo atualizado dinamicamente.

## 🛠️ Tecnologias Utilizadas

  * **Backend**: Python, Flask, Flask-SocketIO
  * **Inteligência Artificial**: LangChain com Google Gemini
  * **Conversão de Texto em Áudio**: Google Cloud Text-to-Speech API
  * **Frontend**: HTML, CSS, JavaScript
  * **Deploy**: Render, Gunicorn

## 💻 Como Rodar o Projeto Localmente

Para testar o projeto na sua própria máquina, siga os passos abaixo:

#### 1\. Pré-requisitos

  * Ter o Python 3 instalado na sua máquina.
  * Ter o `git` instalado para clonar o repositório.

#### 2\. Clone o Repositório

```sh
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio/chat-gabarito/flask_chat
```

#### 3\. Crie e Ative o Ambiente Virtual (`venv`)

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

```sh
# Cria a pasta .venv
python -m venv venv

# Ativa o ambiente no Windows
venv\Scripts\activate

# Ativa o ambiente no macOS ou Linux
source venv/bin/activate
```

#### 4\. Instale as Dependências

Com o ambiente ativado, instale todas as bibliotecas necessárias.

```sh
pip install -r requirements.txt
```

#### 5\. Configure suas Chaves de API

Para a mágica da IA e do áudio acontecer, você precisa de credenciais do Google.

  * **Crie um arquivo `.env`**: Na pasta `chat-gabarito/flask_chat`, crie um arquivo com o nome `.env`.
  * **Adicione a Chave do Gemini**: Dentro do arquivo `.env`, adicione a seguinte linha, substituindo `SUA_CHAVE_API_AQUI` pela sua chave obtida no [Google AI Studio](https://aistudio.google.com/app/apikey).
    ```
    GEMINI_API_KEY=SUA_CHAVE_API_AQUI
    ```
  * **Configure a Chave do Text-to-Speech**:
      * Siga o passo a passo da API do Google Cloud Text-to-Speech (que fizemos anteriormente) para baixar o arquivo de credencial `.json`.
      * Salve este arquivo `.json` em um local seguro no seu computador.
      * Configure uma variável de ambiente no seu sistema chamada `GOOGLE_APPLICATION_CREDENTIALS` que aponte para o caminho completo desse arquivo `.json`.

#### 6\. Rode a Aplicação

Com tudo configurado, inicie o servidor Flask.

```sh
python chatmain.py
```

Abra seu navegador e acesse `http://127.0.0.1:5000` para ver a página inicial.

## 👨‍💻 Equipe

  * Giovanna Andrade Vicentim
  * Hállison Vinicius Vieira Amorim
  * Isaac Maifrino Dias
  * Ruan Pelegrini Lourenço
  * Theo Correia Martins
