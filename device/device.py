import socket
import threading
import time

# Função para receber comandos do servidor via TCP
def receber_do_servidor_tcp(tcp_client):
    while True:
        data = tcp_client.recv(1024)
        if not data:
            break
        print("Comando recebido do servidor TCP:", data.decode())

# Função para enviar dados para o servidor via UDP
def enviar_para_servidor_udp(udp_client):
    while True:
        mensagem = input("Dados UDP")
        udp_client.sendto(mensagem.encode(), (UDP_HOST, UDP_PORT))

# Função para receber comandos do usuário via terminal
def receber_comandos_do_usuario():
    while True:
        comando = input("Digite um comando (ex: 'OFF' para encerrar): ")
        if comando == "OFF":
          # Encerra a conexão UDP
          udp_client.close()
          print('Conexão UDP encerrada')

# Configurações do servidor UDP
UDP_HOST = 'localhost'
UDP_PORT = 8889

# Criação do socket UDP
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Configurações do servidor TCP
TCP_HOST = 'localhost'
TCP_PORT = 8888

# Criação do socket TCP/IP
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta o socket TCP ao servidor
tcp_client.connect((TCP_HOST, TCP_PORT))
print(f'Conectado ao servidor TCP em {TCP_HOST}:{TCP_PORT}')

# Criação das threads
thread_receber_tcp = threading.Thread(target=receber_do_servidor_tcp, args=(tcp_client,))
thread_enviar_udp = threading.Thread(target=enviar_para_servidor_udp, args=(udp_client,))
thread_receber_comandos = threading.Thread(target=receber_comandos_do_usuario)

# Inicia as threads
thread_receber_tcp.start()
thread_enviar_udp.start()
thread_receber_comandos.start()

# Aguarda o término das threads
thread_receber_tcp.join()
thread_enviar_udp.join()
thread_receber_comandos.join()

# Encerra a conexão TCP
tcp_client.close()
print('Conexão TCP encerrada')

# Encerra a conexão UDP
udp_client.close()
print('Conexão UDP encerrada')