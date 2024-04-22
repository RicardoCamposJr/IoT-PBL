import socket
import threading
from flask import Flask, jsonify, request
import pickle
import time
from flask_cors import CORS


IP_SERVER = 'localhost'
UDP_PORT = 8889
TCP_PORT = 8888
socketUDP = ''
socketTCP = ''
transmitterTCPComandThread = ''
# Lista para armazenar os clientes TCP
tcpClients = {}
devices = {}

request1 = True
addr = 'localhost'
# COMANDO E TEMPERATURA
comand = ['ON', 0]

# Função para receber dados via UDP do cliente
def receiveDataUDP():
    global socketUDP
    global devices

    while True:
        data, addr = socketUDP.recvfrom(1024)
        data = pickle.loads(data)
        devices[addr[0]] = {"IPPORT": addr, "message": data["data"], "time": data["time"], "status": data["state"], "deviceName": data["deviceName"]}
        if not data:
            break
        print(f'Mensagem recebida do cliente UDP {addr}: {data}')

# Função para enviar comandos para os clientes via TCP
def sendComandToClientTCP():
    global tcpClients
    global addr
    global comand

    # O addr e o comand virão de uma requisição da interface
    tcpClients[addr[0]]["deviceInfo"].send(pickle.dumps(comand))
    print("comando enviado")

def createSocketUDP():
    global socketUDP
    global IP_SERVER
    global UDP_PORT

    # Criação do socket UDP
    socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Associa o socket com o endereço e a porta
    socketUDP.bind((IP_SERVER, UDP_PORT))
    print(f'Servidor UDP iniciado em {IP_SERVER}:{UDP_PORT}')

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

def createTransmitterTCPComandThread():
    # Inicia a thread para enviar comandos para os clientes via TCP
    transmitterTCPComandThread = threading.Thread(target=sendComandToClientTCP)
    transmitterTCPComandThread.start()

def createReceiverUDPData():
    receiverUDPDataThread = threading.Thread(target=receiveDataUDP)
    receiverUDPDataThread.start()

def createAPIThread():
    APIThread = threading.Thread(target=app.run, args=("localhost", 8082), daemon=True)
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

# main()
createAPIThread()
createSocketTCP()
createSocketUDP()


# Loop principal para aceitar conexões TCP
while True:
    # Aceita conexões de clientes TCP
    tcp_client, addr = socketTCP.accept()
    print(f'Cliente TCP conectado: {addr}')

    # Coloca os dispositivos em um dicionário para o envio de comandos TCP:
    tcpClients[addr[0]] = {"IPPORT": addr, "deviceInfo": tcp_client}

    print(tcpClients.keys())

    # Thread de configuraçao do dispositivo para mostrar o deviceName dele antes de liga-lo na interface.
    # E tambem, para configurar o dicionario que será retornado por HTTP.
    receiverConfigurationThread = threading.Thread(target=receiveDataUDP)
    receiverConfigurationThread.start()
