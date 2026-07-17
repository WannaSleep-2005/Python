hosts = [
    {
        "ip": "192.168.1.10",
        "hostname": "web01",
        "ports": {
            22: "SSH",
            80: "HTTP",
            443: "HTTPS"
        }
    },
    {
        "ip": "192.168.1.20",
        "hostname": "db01",
        "ports": {
            3306: "MySQL",
            22: "SSH"
        }
    }
]

"""
Output:
Host: web01 (192.168.1.10)
  22 -> SSH
  80 -> HTTP
  443 -> HTTPS

Host: db01 (192.168.1.20)
  3306 -> MySQL
  22 -> SSH
"""

for target in hosts:
    print(f"Host: {target['hostname']} ({target['ip']})")

    #for port in target["ports"]:
    #    print(f"  {port} -> {target["ports"][port]}")
    for port, service in target["ports"].items():
        print(f"  {port} -> {service}")