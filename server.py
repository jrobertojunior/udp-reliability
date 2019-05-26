#!/usr/bin/env python3

import socket


def main():
    send_data_to_dns('127.0.0.1')

    # HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    # PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.bind((HOST, PORT))
    #     s.listen()
    #     conn, addr = s.accept()
    #     with conn:
    #         print('Connected by', addr)

    #         while True:
    #             data = conn.recv(1024)

    #             if not data:
    #                 break

    #             msg = "server: received {} ".format(data).encode()
    #             conn.sendall(msg)


def send_data_to_dns(host='127.0.0.1'):
    PORT = 65431

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, PORT))
        s.sendall("www.foo123.org;127.0.0.1".encode())


if __name__ == "__main__":
    main()
