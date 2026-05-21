#!/usr/bin/env python3
"""NFC Reader Simulator — đọc NDEF, giao tiếp ISO 14443"""
import socket, json, time
import ndef
from colorama import Fore, init
init(autoreset=True)

TAG_HOST = '127.0.0.1'
TAG_PORT = 6011

def nfc_cmd(cmd_dict: dict) -> dict:
    s = socket.socket()
    s.settimeout(3)
    s.connect((TAG_HOST, TAG_PORT))
    s.send(json.dumps(cmd_dict).encode())
    resp = json.loads(s.recv(2048).decode())
    s.close()
    return resp

def read_tag_full():
    print(f"{Fore.CYAN}[NFC READER] === Scanning NFC tag ===")
    # Bước 1: REQA — phát hiện tag
    r1 = nfc_cmd({'cmd':'REQA'})
    print(f"{Fore.YELLOW}[NFC READER] ATQA={r1.get('atqa')} SAK={r1.get('sak')}")
    print(f"{Fore.YELLOW}[NFC READER] UID={r1.get('uid','').upper()}")
    # Bước 2: Đọc NDEF content
    r2 = nfc_cmd({'cmd':'READ_NDEF'})
    records = r2.get('records', [])
    if records:
        print(f"{Fore.GREEN}[NFC READER] NDEF Records ({len(records)} found):")
        for i, rec in enumerate(records):
            rtype = rec.get('type','?')
            val   = rec.get('value') or rec.get('data','')
            print(f"  [{i}] {rtype}: {val}")
    else:
        print(f"{Fore.RED}[NFC READER] No NDEF records found")
    return r1, r2

if __name__ == '__main__':
    while True:
        try:
            read_tag_full()
        except Exception as e:
            print(f"{Fore.RED}[NFC READER] No tag: {e}")
        time.sleep(3)
