#!/usr/bin/env python3

import socket
import time

SERVER_DNS = "www.foo123.org"
SERVER_IP = '127.0.0.1'
SERVER_PORT = 65432

DNS_IP = '127.0.0.1'
DNS_PORT = 65431


def main():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    send_address_to_dns(SERVER_DNS, SERVER_IP, SERVER_PORT, DNS_IP, DNS_PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)

            while True:
                data = conn.recv(1024)

                if not data:
                    break

                msg = "server: received {} ".format(data).encode()
                conn.sendall(msg)


def send_address_to_dns(server_dns, server_ip, server_port, dns_ip, dns_port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((dns_ip, dns_port))

        s.sendall("server;{};{};{}".format(
            server_dns, server_ip, server_port).encode())


if __name__ == "__main__":
    main()
