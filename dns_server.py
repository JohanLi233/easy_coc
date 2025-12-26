#!/usr/bin/env python3
"""
简单 DNS 服务器 - 将 game.clashofclans.com 映射到 sqbwiki.com 的 IP
手机设置 DNS 为本机 IP 即可使用
"""

import socket
import struct
import threading
import sys

# 配置
DNS_PORT = 53
LISTEN_IP = "0.0.0.0"  # 监听所有网卡

# sqbwiki.com 的 IP 地址
TARGET_IP = "124.223.85.31"

# DNS 响应配置
TTL = 300

def build_dns_response(data):
    """构建 DNS 响应"""
    # 解析 DNS 请求
    transaction_id = data[:2]

    # 标志位 (QR=1, Opcode=0, AA=0, TC=0, RD=0, RA=1, Z=0, RCODE=0)
    flags = 0x8180  # Standard query response

    # 问题数、答案数、权威附加数
    question_count = 1
    answer_count = 1
    auth_count = 0
    additional_count = 0

    # 构建响应头
    header = transaction_id + struct.pack(">HHHHH", flags, question_count, answer_count, auth_count, additional_count)

    # 问题部分 (复制请求中的问题)
    qstart = 12
    qlen = len(data) - qstart
    question = data[qstart:]

    # 答案部分
    # 格式: 名称(2字节压缩) + 类型(A=1) + 类(IN=1) + TTL + 长度 + IP
    answer = b'\xc0\x0c'  # 压缩的问题名称指针
    answer += struct.pack(">HHIH", 1, 1, TTL, 4)  # Type A, Class IN, TTL, RDLENGTH
    answer += socket.inet_aton(TARGET_IP)  # IP 地址

    return header + question + answer

def handle_dns_query(sock, addr, data):
    """处理单个 DNS 查询"""
    try:
        response = build_dns_response(data)
        sock.sendto(response, addr)
    except Exception as e:
        print(f"处理请求失败: {e}")

def start_dns_server():
    """启动 DNS 服务器"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind((LISTEN_IP, DNS_PORT))
        print(f"DNS 服务器已启动，监听 {LISTEN_IP}:{DNS_PORT}")
        print(f"将 game.clashofclans.com -> {TARGET_IP}")
        print("请将手机的 DNS 设置为本机 IP 地址")

        while True:
            try:
                data, addr = sock.recvfrom(512)
                # 开启新线程处理请求
                thread = threading.Thread(target=handle_dns_query, args=(sock, addr, data))
                thread.daemon = True
                thread.start()
            except Exception as e:
                print(f"接收数据失败: {e}")
    except PermissionError:
        print(f"需要 root 权限运行: sudo python3 {sys.argv[0]}")
    except Exception as e:
        print(f"启动失败: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    print("=" * 50)
    print("COC 国际服 DNS 映射服务器")
    print("=" * 50)

    # 检查 IP 配置
    if TARGET_IP == "0.0.0.0":
        print("警告: 请编辑文件设置正确的 sqbwiki.com IP 地址")

    start_dns_server()
