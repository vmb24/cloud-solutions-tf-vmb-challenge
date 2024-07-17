# Use uma imagem base oficial do Python
FROM python:3.8-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o conteúdo do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Exponha a porta em que a aplicação estará rodando
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "main.py"]
