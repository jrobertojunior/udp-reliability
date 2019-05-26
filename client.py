#!/usr/bin/env python3

import socket

database = {}


def main():
    # show_ui()
    ask_address_to_dns()

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        msg = "client message".encode()

        s.sendall(msg)
        data = s.recv(1024)

    print("client: ", repr(data))


def ask_address_to_dns(host='127.0.0.1', port=65431):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        msg = "client;request;www.foo123.org".encode()
        s.sendall(msg)

        data = s.recv(1024).decode("utf-8")
        # if data == 'ok':
        #     s.sendall("")

        print(data)


def show_ui():
    HORIZ_LINE = "\\\\\\\\\\\\\\\\\\\\"
    SIDE_LINE = ":"

    print(HORIZ_LINE)
    print(SIDE_LINE)
    print(SIDE_LINE, "")


if __name__ == "__main__":
    main()
