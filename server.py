#!/usr/bin/env python3

import socket
import time


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
        s.sendall("server;".encode())
        s.sendall("www.foo123.org;127.0.0.1".encode())

        data = s.recv(1024).decode("utf-8")

        begin = time.perf_counter()
        while True:
            if data == "ok":
                print("cosing server connection with DNS")
                s.sendall("server;bye".encode())

            elif time.perf_counter() - begin > 10:
                print("TIMEOUT - closing connection with DNS")
                break


if __name__ == "__main__":
    main()
