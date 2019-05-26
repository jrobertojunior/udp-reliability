#!/usr/bin/env python3

import socket


def main():

    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65431        # DNS port that I use in this project

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


if __name__ == "__main__":
    main()
