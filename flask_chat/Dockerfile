# 1. Use uma imagem oficial do Python como base
FROM python:3.11-slim

# 2. Instale as dependências de sistema necessárias
#    - apt-get update: Atualiza a lista de pacotes
#    - ffmpeg: Biblioteca essencial para manipulação de áudio e vídeo
RUN apt-get update && apt-get install -y ffmpeg

# 3. Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# 4. Copie o arquivo de dependências do Python para o contêiner
COPY requirements.txt .

# 5. Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copie todo o resto do código da sua aplicação para o contêiner
COPY . .

# 7. Exponha a porta que a aplicação irá usar
EXPOSE 10000

# 8. Defina o comando para iniciar a aplicação quando o contêiner rodar
#    É quase o mesmo comando de antes, mas especificamos o --bind
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:10000", "chatmain:app"]