#!/usr/bin/env python3

import socket

database = {}


def main():
    log("client with ask address to dns")
    ip, port = ask_address_to_dns()

    log("client will start conversation with server")
    tcp_connection_with_server(ip, port)


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


def tcp_connection_with_server(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # print("Client socket created")
        log("Client socket created")

        s.connect((server_ip, server_port))
        log("Connected with {}:{}".format(server_ip, server_port))

        while True:
            op = get_client_input()

            if op == 0:
                s.close()
                return

            msg = op.encode()
            s.sendall(msg)

            data = s.recv(1024).decode("utf-8")

            print(data)


def get_client_input():

    while True:
        HORIZ_LINE = "\\\\\\\\\\"
        SIDE_LINE = ":"

        print("  1. List files")
        print("  0. end connection")

        try:
            possible_ans = [0, 1, 2]
            ans = int(input("  -> "))

            if ans not in possible_ans:
                raise ValueError("some exception here!!")
        except ValueError as e:
            print("input in the wrong format!")
            continue

        return str(ans)


def log(msg):
    print("--", msg)


if __name__ == "__main__":
    main()
