import socket
import threading

IP_SERVER = 'localhost'
UDP_PORT = 8889
TCP_PORT = 8888
socketUDP = ''
socketTCP = ''
transmitterTCPComandThread = ''
# Lista para armazenar os clientes TCP
tcpClients = {}

request = True
addr = 'localhost'
comand = 'ON'

# Função para receber dados via UDP do cliente
def receiveDataUDP():
    global socketUDP

    while True:
        data, addr = socketUDP.recvfrom(1024)
        if not data:
            break
        print(f'Mensagem recebida do cliente UDP {addr}: {data.decode()}')

# Função para enviar comandos para os clientes via TCP
def sendComandToClientTCP():
    global tcpClients
    global addr
    global comand

    # O addr e o comand virão de uma requisição da interface
    tcpClients[addr].send(comand.encode())
  
# Função para receber mensagens dos clientes TCP
def receber_do_cliente_tcp(tcp_client):
    while True:
        data = tcp_client.recv(1024)
        if not data:
            break
        print(f'Mensagem recebida do cliente TCP {tcp_client.getpeername()}: {data.decode()}')

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



# main()
createSocketTCP()
createSocketUDP()


# Loop principal para aceitar conexões TCP
while True:
    # Aceita conexões de clientes TCP
    tcp_client, addr = socketTCP.accept()
    print(f'Cliente TCP conectado: {addr}')

    # Coloca os clientes em um dicionário com o {IP:Cliente}
    tcpClients[addr] = tcp_client

    # Aqui ficaria a request da interface
    if (request == True):
        # Criando a thread responsável por enviar comandos
        createTransmitterTCPComandThread()
        createReceiverUDPData()
