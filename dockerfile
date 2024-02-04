# Usar uma imagem base do Ubuntu
FROM ubuntu:20.04

# Instalar o pacote python3-pip
RUN apt-get update && apt-get install -y python3-pip

# Copiar o arquivo main.py para a pasta /app do contêiner
COPY main.py /app/

# Definir a pasta /app como o diretório de trabalho
WORKDIR /app

# Instalar o framework Flask usando o pip
RUN pip3 install flask

# Definir a variável de ambiente FLASK_APP como main.py
ENV FLASK_APP main.py

# Expor a porta 5000 do contêiner
EXPOSE 5000

# Executar o comando flask run quando o contêiner iniciar
CMD ["flask", "run", "--host=0.0.0.0"]
