import socket
import threading
import time
from datetime import datetime
import pickle
import signal
import sys

choice = 2
serverIP = ''
TCP_PORT = ''
UDP_PORT = ''
deviceName = ''
state = False
mensagem = 21

socketUDP = ''
socketTCP = ''

receiverTCPThread = ''
transmitterUDPThread = ''
verificationThread= ''
changeTempThread = ''

# Funçao caso o programa seja encerrado pelo terminal 
def handler(sig, frame):
    global serverIP
    global UDP_PORT
    global socketUDP
    global choice
    global state
    global deviceName
    global mensagem
    global choice

    print("Programa sendo encerrado...")
    choice = 5
    # Faça aqui o que você precisa antes de sair
    container = {"data": "EXIT", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "state": True, "deviceName": deviceName}
    socketUDP.sendto(pickle.dumps(container), (serverIP, UDP_PORT))
    sys.exit(0)

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

    receiverTCPThread = threading.Thread(target=receiveTCPServer, daemon=True)
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





def connectToServer():
    global serverIP
    global TCP_PORT
    global socketTCP
    global choice

    # Criação do socket TCP
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Tenta conectar ao servidor
    while True:
        try:
            socketTCP.connect((serverIP, TCP_PORT))
            print(f'Conectado ao servidor TCP em {serverIP}:{TCP_PORT}')
            choice = 2
            break  # Se a conexão for bem-sucedida
        except ConnectionRefusedError:
            print("Conexão recusada. Tentando novamente em 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print("Erro ao conectar ao servidor:", e)
            time.sleep(5)






# Função para receber comandos do servidor via TCP
def receiveTCPServer():
    global socketTCP
    global state
    global choice
    global mensagem
    global serverIP
    global TCP_PORT

    # Se choice = 5, significa que o dispositivo foi encerrado pelo terminal (CTRL C)
    while choice != 5:
        try:
            data = socketTCP.recv(1024)
            if not data:
                break
            if pickle.loads(data)[0] == "POWER":
                if state == False:
                    state = True
                    choice = 0
                elif state == True:
                    state = False
                    choice = 2
            if pickle.loads(data)[0] == "SET":
                mensagem = pickle.loads(data)[1]
                state = True
                choice = 0
            if pickle.loads(data)[0] == "FIT":
                fit = True
            print("Comando recebido do servidor TCP:", pickle.loads(data))
        # Caso o broker seja desconectado
        except ConnectionResetError:
            print("O servidor foi desconectado.")
            # Tentar reconectar
            connectToServer()
            

# Função para enviar dados para o servidor via UDP
def transmitterUDPData():
    global serverIP
    global UDP_PORT
    global socketUDP
    global choice
    global state
    global deviceName
    global mensagem

    while choice != 5:
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
connectToServer()
createReceiverTCPThread()
createTransmitterUDPThread()

signal.signal(signal.SIGINT, handler)

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