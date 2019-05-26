#!/usr/bin/env python3

import socket

database = {}


def main():
    show_ui()

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        msg = "client message".encode()

        s.sendall(msg)
        data = s.recv(1024)

    print("client: ", repr(data))


def show_ui():
    HORIZ_LINE = "\\\\\\\\\\\\\\\\\\\\"
    SIDE_LINE = ":"

    print(HORIZ_LINE)
    print(SIDE_LINE)
    print(SIDE_LINE, "")

if __name__ == "__main__":
    main()
