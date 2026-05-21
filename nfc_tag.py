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


if __name__ == '__main__':
    NFCTagServer().run()
