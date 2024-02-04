# Importar módulos necessários
from flask import Flask, request

import socket
import random
import platform
import sys
import subprocess
import os
from multiprocessing import Value

# Criar instância do Flask
app = Flask(__name__)

# Inicializar variáveis globais
num_acessos = Value("i", 0)
num_acessos_simultaneos = Value("i", 0)

# Definir rota para página inicial
@app.route("/")
def informacoes_container():
    with num_acessos.get_lock():
        num_acessos.value += 1

    with num_acessos_simultaneos.get_lock():
        num_acessos_simultaneos.value += 1
        acessos_simultaneos = num_acessos_simultaneos.value

    # Obter informações do contêiner
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    container_id = obter_container_id()
    cor = obter_cor(container_id)
    os_info = platform.system()
    python_version = sys.version

    # Recursos do sistema
    try:
        resource_usage = subprocess.run(["ps", "-eo", "pid,%cpu,%mem,cmd"], capture_output=True, text=True).stdout
    except Exception as e:
        resource_usage = f"Erro ao obter uso de recursos: {e}"

    # Informações de conectividade
    connection_test = "Teste de conectividade bem-sucedido!"

    # Listar arquivos na pasta atual
    try:
        files_list = os.listdir(".")
    except Exception as e:
        files_list = f"Erro ao listar arquivos: {e}"

    # Variáveis de ambiente
    environment_variables = os.environ

    # Informações do Sistema de Arquivos
    try:
        file_system_info = subprocess.run(["df", "-h"], capture_output=True, text=True).stdout
    except Exception as e:
        file_system_info = f"Erro ao obter informações do sistema de arquivos: {e}"

    # Reduzir o número de acessos simultâneos após o processamento da página
    with num_acessos_simultaneos.get_lock():
        num_acessos_simultaneos.value -= 1

    # Retornar página com todas as informações
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Informações do Contêiner</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #4A90E2, #8FBC8F);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    color: #333;
                    transition: background 0.5s ease-in-out;
                }}
                #header-container {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 1rem;
                    width: 100%;
                }}
                header {{
                    background-color: rgba(70, 130, 180, 0.8);
                    text-align: center;
                    color: white;
                    font-size: 2rem;
                    margin-bottom: 20px;
                    flex: 1;
                }}
                #access-info {{
                    background-color: rgba(70, 130, 180, 1);
                    padding: 1rem;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    margin-left: 20px;
                    margin-bottom: 20px;
                    color: white;
                    width: max-content;
                    align-self: flex-start;
                }}
                main {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-evenly;
                    align-items: stretch;
                    gap: 20px;
                    padding: 2rem;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    background-color: rgba(255, 255, 255, 0.8);
                    border-radius: 10px;
                    transition: background-color 0.5s ease-in-out;
                }}
                section {{
                    flex: 1;
                    padding: 1rem;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    background-color: rgba(255, 255, 255, 0.8);
                    margin-bottom: 20px;
                }}
                h2 {{
                    color: #333;
                    font-size: 1.5rem;
                    margin-bottom: 1rem;
                }}
                p {{
                    margin-bottom: 0.5rem;
                }}
                pre {{
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    margin-bottom: 1rem;
                    background-color: #f4f4f4;
                    padding: 1rem;
                    border-radius: 5px;
                }}
                ul {{
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }}
                li {{
                    margin-bottom: 1rem;
                }}
                footer {{
                    background-color: rgba(70, 130, 180, 0.8);
                    padding: 1rem;
                    text-align: center;
                    color: white;
                    font-size: 1rem;
                    margin-top: auto;
                    width: 100%;
                    border-top: 2px solid white;
                }}
            </style>
        </head>
        <body>
            <div id="header-container">
                <header>
                    <h1>Informações do Contêiner</h1>
                </header>
            </div>
            <div id="access-info">
                <p>Acessos: {num_acessos.value}</p>
                <p>Acessos Simultâneos: {acessos_simultaneos}</p>
            </div>
            <main>
                <section>
                    <h2>Informações Gerais:</h2>
                    <p>ID do Contêiner: {container_id}</p>
                    <p>Nome do Host: {hostname}</p>
                    <p>Endereço IP: {ip}</p>
                    <p>Sistema Operacional: {os_info}</p>
                    <p>Versão do Python: {python_version}</p>
                </section>
                <section>
                    <h2>Recursos do Sistema:</h2>
                    <p>Uso de CPU, memória e comandos em execução:</p>
                    <pre>{resource_usage}</pre>
                </section>
                <section>
                    <h2>Informações de Conectividade:</h2>
                    <p>{connection_test}</p>
                </section>
                <section>
                    <h2>Informações do Sistema de Arquivos:</h2>
                    <pre>{file_system_info}</pre>
                </section>
                <section>
                    <h2>Variáveis de Ambiente:</h2>
                    <pre>{environment_variables}</pre>
                </section>
                <section>
                    <h2>Lista de Arquivos na Pasta Atual:</h2>
                    <ul>{''.join([f'<li>{f}</li>' for f in files_list])}</ul>
                </section>
            </main>
            <footer>
                © 2024 Informações do Contêiner
            </footer>
        </body>
        </html>
    """

def obter_cor(container_id):
    # Lógica para obter uma cor única com base no ID do contêiner
    seed_value = hash(container_id) % 0xFFFFFF if container_id else 0
    random.seed(seed_value)
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def obter_container_id():
    try:
        with open("/proc/self/cgroup", "r") as f:
            for line in f:
                if "cpuset" in line or "docker" in line:
                    return line.split("/")[-1].strip()
    except Exception as e:
        print(f"Erro ao obter ID do contêiner: {e}")
        return "Não disponível"

# Executar o aplicativo Flask
if __name__ == "__main__":
    app.run(debug=True)
