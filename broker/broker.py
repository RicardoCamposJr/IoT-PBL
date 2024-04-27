import socket
import threading
from flask import Flask, jsonify, request
import pickle
import time
from flask_cors import CORS

# IP do broker
IP_SERVER = ''
# Porta UDP padrão
UDP_PORT = 8889
# Porta TCP padrão
TCP_PORT = 8888
# Socket UDP
socketUDP = ''
# Socket TCP
socketTCP = ''
# Thread para o envio de comandos TCP para dispositivos
transmitterTCPComandThread = ''
# Lista para armazenar os dispositivos e suas informações de conexão
tcpClients = {}
# Lista para armazenar os dispositivos e suas mensagens
devices = {}

# Função para receber dados via UDP do cliente, utilizada pela thread de recebimento de mensagens
def receiveDataUDP():
    global socketUDP
    global devices
    global tcpClients
    global addr

    socketUDP.settimeout(5)

    while True:
        try:
            data, addr = socketUDP.recvfrom(1024)
            data = pickle.loads(data)
            if data["data"] == "EXIT":
                del devices[addr[0]]
                break
            else:
                devices[addr[0]] = {"IPPORT": addr, "message": data["data"], "time": data["time"], "status": data["state"], "deviceName": data["deviceName"]}
            print(f'Mensagem recebida do cliente UDP {addr}: {data}')

        except socket.timeout:
            try:
                comand = ['FIT', 0]
                if addr[0] in tcpClients:
                    tcpClients[addr[0]]["deviceInfo"].send(pickle.dumps(comand))
            except:
                if addr[0] in devices:
                    del devices[addr[0]]
                print("Tempo limite expirado. Nenhum dado recebido após 5 segundos.")
                break

# Função para enviar comandos para os clientes via TCP, utilizada pela thread de envio de comandos
def sendComandToClientTCP():
    global tcpClients
    global addr
    global comand

    # O addr e o comand virão de uma requisição da interface
    tcpClients[addr[0]]["deviceInfo"].send(pickle.dumps(comand))

# Criação do socket UDP do broker
def createSocketUDP():
    global socketUDP
    global IP_SERVER
    global UDP_PORT

    # Criação do socket UDP
    socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Associa o socket com o endereço e a porta
    socketUDP.bind((IP_SERVER, UDP_PORT))
    print(f'Servidor UDP iniciado em {IP_SERVER}:{UDP_PORT}')

# Criação do socket TCP do broker
def createSocketTCP():
    global socketTCP
    global IP_SERVER
    global TCP_PORT

    # Criação do socket TCP/IP
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Associa o socket com o endereço e a porta
    socketTCP.bind((IP_SERVER, TCP_PORT))
    # Coloca o socket em modo de escuta
    socketTCP.listen()
    print(f'Servidor TCP iniciado em {IP_SERVER}:{TCP_PORT}')

# Thread que envia comandos via TCP para os dispositivos
def createTransmitterTCPComandThread():
    # Inicia a thread para enviar comandos para os clientes via TCP
    transmitterTCPComandThread = threading.Thread(target=sendComandToClientTCP)
    transmitterTCPComandThread.start()

# Thread que recebe dados via UDP dos dispositivos
def createReceiverUDPData():
    receiverUDPDataThread = threading.Thread(target=receiveDataUDP)
    receiverUDPDataThread.start()

# Thread para acionar a API
def createAPIThread():
    APIThread = threading.Thread(target=app.run, args=(str(IP_SERVER), 8082), daemon=True)
    APIThread.start()

#--------------------------------------------------------------------------
#API:
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"], "allow_headers": ["Content-Type", "Authorization"]}})

@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(devices)

@app.route('/power/<string:ip>/', methods=['PATCH'])
def patch_data(ip):
    global comand
    global addr

    comand = ['POWER', 0]

    if ip in devices.keys():
        addr = devices[ip]["IPPORT"]
        createTransmitterTCPComandThread()
    else:
        return "Dispositivo não encontrado"

    time.sleep(1.1)
    return jsonify(devices[ip]), 200

@app.route('/set/<string:ip>/<int:temp>', methods=['PATCH'])
def set_temp(ip, temp):
    global comand
    global addr

    comand = ['SET', temp]

    if ip in devices.keys():
        addr = devices[ip]["IPPORT"]
        createTransmitterTCPComandThread()
    else:
        return "Dispositivo não encontrado"

    time.sleep(1.1)
    return jsonify(devices[ip]), 200

#--------------------------------------------------------------------------

# Configuração do IP do broker
IP_SERVER = str(input("Insira o IP deste servidor: "))
# Criação da thread da API
createAPIThread()
# Criação do socket TCP
createSocketTCP()
# Criação do socket UDP
createSocketUDP()


# Loop principal para aceitar conexões TCP
while True:
    # Aceita conexões de clientes TCP
    tcp_client, addr = socketTCP.accept()
    print(f'Cliente TCP conectado: {addr}')

    # Coloca os dispositivos em um dicionário para o envio de comandos TCP
    tcpClients[addr[0]] = {"IPPORT": addr, "deviceInfo": tcp_client}

    # Criação de uma thread para o dispositivo conectado
    receiverConfigurationThread = threading.Thread(target=receiveDataUDP)
    receiverConfigurationThread.start()
