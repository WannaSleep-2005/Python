import socket

target_host = "192.168.3.56"
target_port = 9000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    client.connect((target_host, target_port))
    client.send(input("Enter message to send: ").encode())
    response = client.recv(4096)
    print(response.decode())
    client.close()