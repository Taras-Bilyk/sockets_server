import socket
import config
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_to_server(data):
    data_to_send = str(data)
    server_ip = str(config.server_ip)
    server_port = int(config.server_port)
    s.sendto(data_to_send.encode(), (server_ip, server_port))

