hosts = {
    "192.168.1.10": [22, 80, 443],
    "192.168.1.20": [21, 22],
    "192.168.1.30": [3306, 8080]
}

"""
Host: 192.168.1.10
  Open Port: 22
  Open Port: 80
  Open Port: 443

Host: 192.168.1.20
  Open Port: 21
  Open Port: 22

Host: 192.168.1.30
  Open Port: 3306
  Open Port: 8080
"""

for key, value in hosts.items():
    print(f"Host: {key}")
    for i in value:
        print(f"  Open Port: {i}")
