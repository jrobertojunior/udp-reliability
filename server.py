#!/usr/bin/env python3

import socket
import time
import os
from support import *

DOMAIN = "www.foo123.org"
SERVER_IP = 'localhost'
SERVER_PORT = 65432
THIS_ADDR = ("localhost", 65432)

DNS_IP = 'localhost'
DNS_PORT = 65431
DNS_ADDR = ('localhost', 65431)

def main():
    log("will send this domain address to DNS server")
    send_address_to_dns(DOMAIN, SERVER_IP, SERVER_PORT, DNS_ADDR)

    log("server will start communication with client")
    udp_with_client(THIS_ADDR)

    print("END OF PROGRAM")


def send_address_to_dns(server_dns, server_ip, server_port, dns_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        msg = "server;{};{};{}".format(server_dns, server_ip, server_port).encode()
        s.sendto(msg, DNS_ADDR)

        print("  -> {} to {}".format(msg.decode("utf-8"), DNS_ADDR))


def tcp_connetion_with_client(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_ip, server_port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)

            while True:
                data = conn.recv(1024)

                if not data:
                    break

                msg = "server: received {} ".format(data).encode()
                client_msg = data.decode("utf-8")

                send_msg = None
                if client_msg == "1":
                    conn.sendall(get_list_files().encode())

def udp_with_client(client_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)
        while True:
            data, addr = s.recvfrom(1024)
            print("  <- {} from {}".format(data.decode("utf-8"), addr))

            msg_received = data.decode("utf-8")

            if msg_received == "1":
                msg = str(os.listdir("./server_data"))
                s.sendto(msg.encode(), client_addr)
                print_sent(msg, client_addr)

def get_list_files():
    files = os.listdir("./server_data")

    msg = ""
    i = 1
    for f in files:
        msg += "{}. {}\n".format(i, f)
        i += 1

    return msg

def log(msg):
    print("-", msg)

if __name__ == "__main__":
    main()
