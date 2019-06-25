#!/usr/bin/env python3

import socket
import time
import os

SERVER_DNS = "www.foo123.org"
SERVER_IP = 'localhost'
SERVER_PORT = 65432

DNS_IP = 'localhost'
DNS_PORT = 65431
DNS_ADDR = ('localhost', 65431)

def main():
    print("log: server will send address to DNS server".upper())
    send_address_to_dns(SERVER_DNS, SERVER_IP, SERVER_PORT, DNS_IP, DNS_PORT)

    print("log: server will start communication with client".upper())
    tcp_connetion_with_client(SERVER_IP, SERVER_PORT)

    print("END OF PROGRAM")


def send_address_to_dns(server_dns, server_ip, server_port, dns_ip, dns_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        msg = "server;{};{};{}".format(server_dns, server_ip, server_port).encode()
        s.sendto(msg, DNS_ADDR)

        print("  -> {} to {}".format(msg, DNS_ADDR))

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((dns_ip, dns_port))
    #     print("Connected with {}:{}".format(dns_ip, dns_port))

    #     msg = "server;{};{};{}".format(server_dns, server_ip, server_port)
    #     s.sendall(msg.encode())

    #     print("  sent")
    #     print("  ->", msg)


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


def get_list_files():
    files = os.listdir("./server_data")

    msg = ""
    i = 1
    for f in files:
        msg += "{}. {}\n".format(i, f)
        i += 1

    return msg


if __name__ == "__main__":
    main()
