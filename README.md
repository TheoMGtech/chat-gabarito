
# 🧠 Aplicativo Web de Atendimento com IA

Este projeto é um aplicativo web desenvolvido com Flask, LangChain e a API gratuita do Gemini, que conecta um usuário e um atendente em tempo real. Ele possui um assistente inteligente que responde quando o usuário digita o comando especial `#Chat`, além de uma funcionalidade para converter respostas em áudio usando `pyttsx3` e `socketio`.
## Funcionalidades

- Conexão em tempo real entre o usuário e o atendente

- Comando especial `#Chat` ativa a resposta da IA Gemini

- Sistema de juiz que valida ou corrige a resposta da IA

- Botão "Ativar Áudio" converte a resposta da IA em fala com `Pyttsx3`

- Comunicação em tempo real com `flask-socketio`
## Tecnologias Utilizadas
- [Flask](https://flask.palletsprojects.com/)

- [LangChain](https://www.langchain.com/)

- [API Gemini](https://ai.google.dev/) (versão gratuita)

- [Pyttsx3](https://pyttsx3.readthedocs.io/en/latest/) (Síntese de fala)

- [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) (Comunicação em tempo real)
## Instalação

Instale flask-chat com pip

```sh
    # Clone o repositório
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio

    # Crie um ambiente virtual (opcional, mas recomendado)
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`

    # Instale as dependências
    pip install -r requirements.txt

```
    
## Execução

```bash
    # Inicie o servidor Flask
    python app.py
```
## Como funciona
1. O usuário se conecta a um atendente ou usuário através da interface de chat.

2. Quando digita `#Chat` dentro da área do usuário, seguido de uma pergunta, a mensagem é redirecionada para a IA Gemini via `LangChain`.

3. A resposta é avaliada ou corrigida por um módulo de Juiz.

4. Se o usuário clicar em "Ativar Áudio", a resposta é convertida em áudio com `pyttsx3` e enviada em tempo real via socketio.
## Melhorias 📌
- Adicionar sistema de login/autenticação

- Melhorar a interface com frameworks de frontend

- Suporte a múltiplos idiomas

- Implantação em nuvem (ex: Render, Railway, ou Heroku)
## Autores

- [@TheoMGtech](https://github.com/TheoMGtech)
- [@isaacnewthon-tech](https://github.com/isaacnewton-tech)
- [@hallisonamorim](https://github.com/hallisonamorim)
- [@gigerminare](https://github.com/gigerminare)
- [@ruan-lourenco](https://github.com/ruan-lourenco)





## Licença

[MIT](https://choosealicense.com/licenses/mit/)

