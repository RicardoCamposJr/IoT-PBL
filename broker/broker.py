import socket
import threading

# Função para lidar com a comunicação UDP com um cliente
def handle_udp_client(client_address):
    while True:
        data, addr = udp_server.recvfrom(1024)
        if not data:
            break
        print(f'Mensagem recebida do cliente UDP {addr}: {data.decode()}')

# Função para enviar comandos para os clientes via TCP
def sendComandToClientTCP(addr, comand):
  tcp_clients[addr].sendall(comand.encode())
  
# Função para receber mensagens dos clientes TCP
def receber_do_cliente_tcp(tcp_client):
    while True:
        data = tcp_client.recv(1024)
        if not data:
            break
        print(f'Mensagem recebida do cliente TCP {tcp_client.getpeername()}: {data.decode()}')

# Configurações do servidor UDP
UDP_HOST = 'localhost'
UDP_PORT = 8889

# Criação do socket UDP
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket com o endereço e a porta
udp_server.bind((UDP_HOST, UDP_PORT))

print(f'Servidor UDP iniciado em {UDP_HOST}:{UDP_PORT}')

# Lista para armazenar os clientes TCP
tcp_clients = {}

# Configurações do servidor TCP
TCP_HOST = 'localhost'
TCP_PORT = 8888

# Criação do socket TCP/IP
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket com o endereço e a porta
tcp_server.bind((TCP_HOST, TCP_PORT))

# Coloca o socket em modo de escuta
tcp_server.listen()

print(f'Servidor TCP iniciado em {TCP_HOST}:{TCP_PORT}')

addr = 'localhost'
comand = 'ON'



# Loop principal para aceitar conexões TCP
while True:
    # Aceita conexões de clientes TCP
    tcp_client, addr = tcp_server.accept()
    print(f'Cliente TCP conectado: {addr}')

    # Coloca os clientes em um dicionário com o {IP:Cliente}
    tcp_clients[addr] = tcp_client

    # Inicia a thread para enviar comandos para os clientes via TCP
    thread_enviar_comandos_tcp = threading.Thread(target=sendComandToClientTCP(addr, comand))
    thread_enviar_comandos_tcp.start()

    # Inicia uma nova thread para lidar com o cliente TCP
    # client_thread = threading.Thread(target=receber_do_cliente_tcp, args=(tcp_client, addr))
    # client_thread.start()


    print(tcp_clients)

