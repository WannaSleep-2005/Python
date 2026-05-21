#!/usr/bin/env python3
"""RFID Reader Simulator — đầu đọc RFID gửi query định kỳ"""
import socket, json, time
from colorama import Fore, Style, init
init(autoreset=True)

TAG_HOST = '127.0.0.1'
TAG_PORT = 6001
AC_HOST  = '127.0.0.1'
AC_PORT  = 7001

class RFIDReader:
    def __init__(self):
        self.scan_interval = 2.0   # giây giữa mỗi lần quét
        self.log = []

    def query_tag(self):
        """Gửi QUERY tới tag và nhận UID"""
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect((TAG_HOST, TAG_PORT))
            s.send(json.dumps({'cmd':'QUERY'}).encode())
            resp = json.loads(s.recv(512).decode())
            s.close()
            return resp
        except Exception:
            return None

    def authenticate_with_ac(self, uid: str) -> dict:
        """Gửi UID lên Access Control Server để xác thực"""
        try:
            s = socket.socket()
            s.settimeout(3)
            s.connect((AC_HOST, AC_PORT))
            payload = {'cmd':'AUTH','uid':uid,'timestamp':time.time()}
            s.send(json.dumps(payload).encode())
            resp = json.loads(s.recv(512).decode())
            s.close()
            return resp
        except Exception as e:
            return {'status':'ERROR','msg':str(e)}

    def run(self):
        print(f"{Fore.CYAN}[READER] RFID Reader started, scanning every {self.scan_interval}s")
        while True:
            tag_resp = self.query_tag()
            if tag_resp and tag_resp.get('status') == 'TAG_PRESENT':
                uid = tag_resp['uid']
                print(f"{Fore.YELLOW}[READER] Tag detected: UID={uid} RSSI={tag_resp.get('rssi')}")
                # Xác thực với Access Control
                ac_resp = self.authenticate_with_ac(uid)
                if ac_resp.get('status') == 'GRANTED':
                    print(f"{Fore.GREEN}[READER] ACCESS GRANTED — {ac_resp.get('owner')}")
                else:
                    print(f"{Fore.RED}[READER] ACCESS DENIED — {ac_resp.get('msg','Unknown')}")
            else:
                print(f"{Fore.WHITE}[READER] No tag in range")
            time.sleep(self.scan_interval)

if __name__ == '__main__':
    RFIDReader().run()
