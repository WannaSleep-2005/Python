#!/usr/bin/env python3
"""NFC Tag Simulator — NTAG213 / MIFARE Ultralight với NDEF"""
import socket, json, time, struct
import ndef
from colorama import Fore, init
init(autoreset=True)

HOST = '127.0.0.1'
PORT = 6011

def make_uri_record(url: str) -> bytes:
    """Tạo NDEF URI record"""
    record = ndef.UriRecord(url)
    return b''.join(ndef.message_encoder([record]))

def make_text_record(text: str, lang='vi') -> bytes:
    record = ndef.TextRecord(text, language=lang)
    return b''.join(ndef.message_encoder([record]))

def make_vcard_record() -> bytes:
    vcard = (
        'BEGIN:VCARD\nVERSION:3.0\n'
        'FN:Dinh Manh Duc\nORG:IoT Lab\n'
        'TEL:+84901234567\nEMAIL:duc@iotlab.edu.vn\n'
        'END:VCARD'
    )
    record = ndef.MimeRecord('text/vcard', vcard.encode())
    return b''.join(ndef.message_encoder([record]))

# ── Bộ nhớ tag NTAG213 (180 byte user memory, 45 pages x 4 byte) ─
class NTAG213:
    def __init__(self):
        self.uid    = bytes([0x04,0xA1,0xB2,0xC3,0xD4,0xE5,0xF6])  # 7-byte UID
        self.pages  = bytearray(45 * 4)                             # 180 byte
        # Ghi NDEF message vào page 4 trở đi
        ndef_data = make_uri_record('https://iotlab.edu.vn/checkin')
        self.pages[16:16+len(ndef_data)] = ndef_data
        self.lock_bytes = bytearray(2)   # Chưa lock — ai cũng ghi được
        self.pw_auth    = False           # Password auth tắt (lỗ hổng)

    def read_page(self, page_no: int) -> bytes:
        offset = page_no * 4
        return bytes(self.pages[offset:offset+4])

    def write_page(self, page_no: int, data: bytes):
        if self.lock_bytes[0] & (1 << page_no):
            raise ValueError(f'Page {page_no} is locked')
        offset = page_no * 4
        self.pages[offset:offset+4] = data[:4]

    def read_all_ndef(self) -> list:
        try:
            return list(ndef.message_decoder(bytes(self.pages[16:80])))
        except Exception:
            return []

class NFCTagServer:
    def __init__(self):
        self.tag    = NTAG213()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(5)
        print(f"{Fore.GREEN}[NFC TAG] NTAG213 simulator @ {HOST}:{PORT}")
        print(f"{Fore.YELLOW}[NFC TAG] UID={self.tag.uid.hex().upper()}")

    def handle(self, conn, addr):
        import threading
        print(f"{Fore.CYAN}[NFC TAG] Reader connected: {addr}")
        try:
            while True:
                data = conn.recv(512)
                if not data: break
                req  = json.loads(data.decode())
                cmd  = req.get('cmd','')
                resp = {}

                if cmd == 'REQA':           # ISO 14443 Request Type A
                    resp = {'atqa':'0x4400','sak':'0x00','uid':self.tag.uid.hex()}
                elif cmd == 'GET_UID':
                    resp = {'uid': self.tag.uid.hex().upper(),
                            'uid_len': len(self.tag.uid)}
                elif cmd == 'READ_PAGE':
                    pg   = req.get('page', 4)
                    data_read = self.tag.read_page(pg)
                    resp = {'page':pg,'data':data_read.hex()}
                elif cmd == 'READ_NDEF':
                    records = self.tag.read_all_ndef()
                    parsed  = []
                    for r in records:
                        if isinstance(r, ndef.UriRecord):
                            parsed.append({'type':'URI','value':r.iri})
                        elif isinstance(r, ndef.TextRecord):
                            parsed.append({'type':'TEXT','value':r.text})
                        elif isinstance(r, ndef.MimeRecord):
                            parsed.append({'type':'MIME','mime':r.type,
                                           'data':r.data.decode(errors='replace')})
                    resp = {'records': parsed}
                elif cmd == 'WRITE_NDEF':
                    # Ghi NDEF mới — không kiểm tra quyền (lỗ hổng)
                    new_ndef = bytes.fromhex(req.get('ndef_hex',''))
                    page_start = 4
                    for i in range(0, len(new_ndef), 4):
                        chunk = new_ndef[i:i+4].ljust(4, b'\x00')
                        self.tag.write_page(page_start + i//4, chunk)
                    resp = {'status':'WRITTEN','bytes':len(new_ndef)}
                    print(f"{Fore.RED}[NFC TAG] ⚠ NDEF OVERWRITTEN by {addr}")
                else:
                    resp = {'status':'ERROR','msg':'Unknown NFC command'}

                conn.send(json.dumps(resp).encode() + b'\n')
        except Exception as e:
            print(f"{Fore.RED}[NFC TAG] Error: {e}")
        finally:
            conn.close()

    def run(self):
        import threading
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handle,args=(conn,addr),daemon=True).start()

if __name__ == '__main__':
    NFCTagServer().run()
