hosts = {
    "192.168.1.10": {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS"
    },
    "192.168.1.20": {
        21: "FTP",
        22: "SSH"
    }
}

"""
Output:
Host: 192.168.1.10
  22 -> SSH
  80 -> HTTP
  443 -> HTTPS

Host: 192.168.1.20
  21 -> FTP
  22 -> SSH
"""

for ip, ports in hosts.items():
    print(f"Host: {ip}")
    for port, service in ports.items():
        print(f"  {port} -> {service}")
