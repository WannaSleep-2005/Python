#!/usr/bin/env python3
"""RFID Tag Simulator — mô phỏng thẻ EM4100 / HID Prox qua TCP"""
import socket, json, time, struct, hashlib
from colorama import Fore, Style, init
init(autoreset=True)

HOST = '127.0.0.1'
PORT = 6001

# ── Dữ liệu thẻ RFID mô phỏng ──────────────────────────────
CARDS = {
    'CARD_001': {
        'uid'        : 'A1B2C3D4E5',      # UID 40-bit hex (không có auth)
        'type'       : 'EM4100',
        'facility'   : 12,                 # HID facility code
        'card_number': 3456,               # HID card number
        'owner'      : 'Dinh Manh Duc',
        'access_level': 'EMPLOYEE',
    },
    'CARD_002': {
        'uid'        : 'DEADBEEF01',
        'type'       : 'HID_PROX',
        'facility'   : 12,
        'card_number': 7890,
        'owner'      : 'Nguyen Nguyen Khuyen',
        'access_level': 'ADMIN',
    },
}

def encode_em4100(uid_hex: str) -> bytes:
    """Tạo frame EM4100 từ UID hex string (5 byte)"""
    uid_bytes = bytes.fromhex(uid_hex)
    # Header 9 bit (0xFF, 0x80), 40 bit data, 14 bit parity (simplified)
    frame = b'\xFF\x80' + uid_bytes + b'\x00\x00'
    return frame

class RFIDTagServer:
    def __init__(self, card_id='CARD_001'):
        self.card    = CARDS[card_id]
        self.card_id = card_id
        self.server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(5)
        print(f"{Fore.GREEN}[TAG] RFID Tag online @ {HOST}:{PORT}")
        print(f"{Fore.YELLOW}[TAG] UID={self.card['uid']} Owner={self.card['owner']}")

    def handle_client(self, conn, addr):
        print(f"{Fore.CYAN}[TAG] Reader connected from {addr}")
        try:
            while True:
                data = conn.recv(256)
                if not data: break
                req = json.loads(data.decode())
                cmd = req.get('cmd','')

                if cmd == 'QUERY':
                    # Thẻ RFID 125kHz phát UID không cần hỏi — luôn phát
                    resp = {
                        'status' : 'TAG_PRESENT',
                        'uid'    : self.card['uid'],     # Lỗ hổng: UID không mã hóa
                        'type'   : self.card['type'],
                        'frame'  : encode_em4100(self.card['uid']).hex(),
                        'rssi'   : -42,                 # Mô phỏng tín hiệu RF
                    }
                elif cmd == 'ANTI_COLLISION':
                    resp = {'status':'OK','uid':self.card['uid']}
                elif cmd == 'GET_INFO':
                    resp = {
                        'owner'       : self.card['owner'],   # Lỗ hổng: lộ thông tin
                        'access_level': self.card['access_level'],
                        'facility'    : self.card['facility'],
                        'card_number' : self.card['card_number'],
                    }
                else:
                    resp = {'status':'ERROR','msg':'Unknown command'}

                conn.send(json.dumps(resp).encode() + b'\n')
        except Exception as e:
            print(f"{Fore.RED}[TAG] Error: {e}")
        finally:
            conn.close()

    def run(self):
        import threading
        print(f"{Fore.GREEN}[TAG] Waiting for readers...")
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handle_client,
                             args=(conn,addr), daemon=True).start()

if __name__ == '__main__':
    import sys
    card_id = sys.argv[1] if len(sys.argv)>1 else 'CARD_001'
    RFIDTagServer(card_id).run()
