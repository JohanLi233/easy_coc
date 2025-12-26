#!/usr/bin/env python3

import socket
import struct
import threading
import sys

DNS_PORT = 53
LISTEN_IP = "0.0.0.0"

TARGET_DOMAIN = b"game.clashofclans.com"
TARGET_IP = "124.223.85.31"
TTL = 300

def parse_qname(data):
    labels = []
    idx = 12
    while True:
        length = data[idx]
        if length == 0:
            idx += 1
            break
        labels.append(data[idx + 1: idx + 1 + length])
        idx += 1 + length
    qname = b".".join(labels)
    qtype, qclass = struct.unpack(">HH", data[idx:idx + 4])
    return qname, qtype, qclass, idx + 4

def build_response(data):
    transaction_id = data[:2]
    flags = 0x8180

    qname, qtype, qclass, qend = parse_qname(data)
    if qtype != 1 or qclass != 1:
        return None
    if qname.lower() != TARGET_DOMAIN:
        return None

    header = transaction_id + struct.pack(">HHHHH", flags, 1, 1, 0, 0)
    question = data[12:qend]

    answer = b"\xc0\x0c"
    answer += struct.pack(">HHIH", 1, 1, TTL, 4)
    answer += socket.inet_aton(TARGET_IP)

    return header + question + answer

def handle_query(sock, addr, data):
    try:
        resp = build_response(data)
        if resp:
            sock.sendto(resp, addr)
    except Exception as e:
        print(e)

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((LISTEN_IP, DNS_PORT))

    print(f"DNS listening on {LISTEN_IP}:{DNS_PORT}")
    print(f"{TARGET_DOMAIN.decode()} -> {TARGET_IP}")

    while True:
        data, addr = sock.recvfrom(512)
        t = threading.Thread(target=handle_query, args=(sock, addr, data))
        t.daemon = True
        t.start()

if __name__ == "__main__":
    try:
        start_server()
    except PermissionError:
        print(f"need root: sudo python3 {sys.argv[0]}")

