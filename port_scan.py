import sys
import socket
import pyfiglet

banner = pyfiglet.figlet_format("PORT SCANNER")
print(banner)

ip = '192.168.1.3'
open_ports = []
ports = range(1, 65535)

def scan(ip, port, result = 1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        r = sock.connect_ex((ip, port))
        if r == 0:
            result = r
        sock.close()
    except Exception as e:
        pass
    return result

for port in ports:
    sys.stdout.flush()
    res = scan(ip, port)
    if res == 0:
        open_ports.append(port)
    
if open_ports:
    print("Open ports: ")
    print(sorted(open_ports))
else:
    print("No port")