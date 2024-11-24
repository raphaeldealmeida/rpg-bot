FROM python:3.10.12-slim

# Configuração de ambiente
ENV POETRY_VIRTUALENVS_CREATE=false

# Define um diretório de trabalho absoluto
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Define o comando a ser executado quando o container iniciar
CMD ["python", "bot.py"]
