#!/usr/bin/env python3

import socket

database = {}


def main():
    server_address = ask_address_to_dns()
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65431        # The port used by the server

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     print("Client socket created")

    #     s.connect((HOST, PORT))
    #     print("Connected with {}:{}".format(HOST, PORT))

    #     msg = "client;www.foo123.org".encode()
    #     s.sendall(msg)

    #     data = s.recv(1024).decode("utf-8")

    #     print(data)


def ask_address_to_dns(host='127.0.0.1', port=65431):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Client socket created")

        s.connect((host, port))

        print("Connected with {}:{}".format(host, port))

        request = "www.foo123.org"
        msg = "client;{}".format(request).encode()
        s.sendall(msg)

        print("Requested", request)

        data = s.recv(1024).decode("utf-8")

        print("  -> received", data)

    return data


def show_ui():
    HORIZ_LINE = "\\\\\\\\\\\\\\\\\\\\"
    SIDE_LINE = ":"

    print(HORIZ_LINE)
    print(SIDE_LINE)
    print(SIDE_LINE, "")


if __name__ == "__main__":
    main()
