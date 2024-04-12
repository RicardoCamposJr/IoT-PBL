import socket
import threading
import time

comand = True
choice = ''
serverIP = ''
TCP_PORT = ''
UDP_PORT = ''

socketUDP = ''
socketTCP = ''

receiverTCPThread = ''
transmitterUDPThread = ''

# Conecta o socket TCP ao broker
def connectSocketTCP():
    global socketTCP
    global TCP_PORT

    socketTCP.connect((serverIP, TCP_PORT))
    print(f'Conectado ao servidor TCP em {serverIP}:{TCP_PORT}')

# Cria os sockets TCP e UDP
def createSockets():
    global socketUDP
    global socketTCP

    # Criação do socket UDP
    socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Criação do socket TCP/IP
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Cria e roda a thread de recebimento de comandos via TCP
def createReceiverTCPThread():
    global receiverTCPThread

    receiverTCPThread = threading.Thread(target=receiveTCPServer)
    receiverTCPThread.start()

# Cria e roda a thread de envio de dados via UDP
def createTransmitterUDPThread():
    global transmitterUDPThread

    transmitterUDPThread = threading.Thread(target=transmitterUDPData)
    transmitterUDPThread.start()

# Função para receber comandos do servidor via TCP
def receiveTCPServer():
    global socketTCP
    while True:
        data = socketTCP.recv(1024)
        if not data:
            break
        print("Comando recebido do servidor TCP:", data.decode())

# Função para enviar dados para o servidor via UDP
def transmitterUDPData():
    global serverIP
    global UDP_PORT
    global socketUDP
    global choice

    while True:
        # Caso o usuário escolha desligar o dispositivo
        if (choice == 2):
            print("\nDispositivo desligado. Envio de dados cancelado.\nInsira seu comando: ")
            break
        mensagem = ("Mensagem UDP")
        socketUDP.sendto(mensagem.encode(), (serverIP, UDP_PORT))
        time.sleep(3)

# Menu inicial de configuração do dispositivo
def menuConfig():
    global TCP_PORT
    global UDP_PORT
    global serverIP

    print("Configure seu dispositivo:")
    serverIP = input("IP do Servidor: ")
    UDP_PORT = int(input("Porta UDP: "))
    TCP_PORT = int(input("Porta TCP: "))

# Controle do dispositivo pelo usuário via terminal
def menuComand() :
    global choice
    global comand

    choice = int(input("\nBem vindo seu dispositivo!\n[0] - Ligar\n[1] - Definir temperatura\n[2] - Desligar\n"))
    if choice == 0:
        # Iniciando o envio de dados via UDP:
        createTransmitterUDPThread()


# Configurando o dispositivo antes de iniciá-lo:
menuConfig()
createSockets()
connectSocketTCP()
createReceiverTCPThread()

# main()
# Início da manipulação do dispositivo pelo usuário via terminal
while (comand):
    menuComand()


# Encerra a conexão TCP
socketTCP.close()
print('Conexão TCP encerrada')

# Encerra a conexão UDP
socketUDP.close()
print('Conexão UDP encerrada')