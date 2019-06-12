#!/usr/bin/env python3

import socket

database = {}


def main():
    ip, port = ask_address_to_dns()

    if ip != -1 and port != -1:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Client socket created")

            s.connect((ip, port))
            print("Connected with {}:{}".format(ip, port))

            msg = "client;www.foo123.org".encode()
            s.sendall(msg)

            data = s.recv(1024).decode("utf-8")

            print(data)


def ask_address_to_dns(host='127.0.0.1', port=65431, dns="www.foo123.org"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Client socket created")

        s.connect((host, port))

        print("Connected with {}:{}".format(host, port))

        dns = "www.foo123.org"
        msg = "client;{}".format(dns).encode()
        s.sendall(msg)

        print("Requested", dns)

        data = s.recv(1024).decode("utf-8")

        print("  -> received", data)

    if data == "null":
        print("The DNS {} was not found in the database".format(dns))
        return -1, -1

    data = data.replace('(', "")
    data = data.replace(')', "")
    data = data.replace('\'', "")
    data = data.replace(' ', "")

    ip, port = data.split(',')

    return ip, int(port)


def show_ui():
    HORIZ_LINE = "\\\\\\\\\\\\\\\\\\\\"
    SIDE_LINE = ":"

    print(HORIZ_LINE)
    print(SIDE_LINE)
    print(SIDE_LINE, "")


if __name__ == "__main__":
    main()
