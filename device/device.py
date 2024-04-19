import socket
import threading
import time
from datetime import datetime
import pickle

choice = 2
serverIP = ''
TCP_PORT = ''
UDP_PORT = ''
deviceName = ''
state = False
setTemp = False
variavel = ''
mensagem = 21

socketUDP = ''
socketTCP = ''

receiverTCPThread = ''
transmitterUDPThread = ''
verificationThread= ''
changeTempThread = ''

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

    transmitterUDPThread = threading.Thread(target=transmitterUDPData, daemon=True)
    transmitterUDPThread.start()

def createChangeTempThread():
    global changeTempThread

    changeTempThread = threading.Thread(target=listenChangeTemp, daemon=True)
    changeTempThread.start()
    changeTempThread.join()

def listenChangeTemp():
    global mensagem
    global choice

    while choice == 1:
        global mensagem
        mensagem = int(input("Insira a temperatura: "))
        choice = 0

# Função para receber comandos do servidor via TCP
def receiveTCPServer():
    global socketTCP
    global state
    global choice
    while True:
        data = socketTCP.recv(1024)
        if not data:
            break
        if data.decode() == "POWER":
            if state == False:
                state = True
                choice = 0
            elif state == True:
                state = False
                choice = 2
        print("Comando recebido do servidor TCP:", data.decode())
        print(state)

# Função para enviar dados para o servidor via UDP
def transmitterUDPData():
    global serverIP
    global UDP_PORT
    global socketUDP
    global choice
    global state
    global deviceName
    global setTemp
    global mensagem

    while True:
        # Caso o usuário escolha desligar o dispositivo
        if (choice == 2):
            state = False
            container = {"data": "Dispositivo desligado.", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "state": False, "deviceName": deviceName}
            socketUDP.sendto(pickle.dumps(container), (serverIP, UDP_PORT))
            print("\nDispositivo desligado.\nInsira seu comando: ")
            choice = 3
        if choice == 0 or choice == 1:
            if choice == 1:
                createChangeTempThread()
                choice = 0
            state = True
            container = {"data": mensagem, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "state": True, "deviceName": deviceName}
            socketUDP.sendto(pickle.dumps(container), (serverIP, UDP_PORT))
            time.sleep(1)
            

# Menu inicial de configuração do dispositivo
def menuConfig():
    global TCP_PORT
    global UDP_PORT
    global serverIP
    global deviceName

    print("Configure seu dispositivo:")
    serverIP = input("IP do Servidor: ")
    UDP_PORT = int(input("Porta UDP: "))
    TCP_PORT = int(input("Porta TCP: "))
    deviceName = input("Nome do dispositivo: ")

# Controle do dispositivo pelo usuário via terminal
def menuComand() :
    global choice
    if choice != 1:
        choice = int(input("\nBem vindo seu dispositivo!\n[0] - Ligar\n[1] - Definir temperatura\n[2] - Desligar\n"))
    
    

# Configurando o dispositivo antes de iniciá-lo:
menuConfig()
createSockets()
connectSocketTCP()
createReceiverTCPThread()
createTransmitterUDPThread()

# main()
# Início da manipulação do dispositivo pelo usuário via terminal
while (True):
    menuComand()
    


# Encerra a conexão TCP
socketTCP.close()
print('Conexão TCP encerrada')

# Encerra a conexão UDP
socketUDP.close()
print('Conexão UDP encerrada')