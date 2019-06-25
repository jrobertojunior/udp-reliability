#!/usr/bin/env python3

import socket

database = {}

DNS_ADDR = ('localhost', 65431)

THIS_ADDR = ("localhost", 65430)

def main():
    log("client with ask address to dns")
    addr = ask_address_to_dns()

    log("client will start conversation with server")
    udp_with_server(addr)


def ask_address_to_dns(domain="www.foo123.org"):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)

        msg = "client;{}".format(domain).encode()

        s.sendto(msg, DNS_ADDR) # send dns request message
        print_sent(msg, DNS_ADDR)
        # print("  -> {} to {}".format(msg.decode("utf-8"), dns_server_addr))

        data, addr = s.recvfrom(1024)
        print_received(data, addr)
        # print("  <- {} from {}".format(msg_received, addr))

        return handle_dns_message(data)
    

def handle_dns_message(data):
    data = data.decode("utf-8")
    data = data.replace('(', "")
    data = data.replace(')', "")
    data = data.replace('\'', "")
    data = data.replace(' ', "")

    ip, port = data.split(',')

    return (ip, int(port))


def tcp_connection_with_server(server_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # print("Client socket created")
        log("Client socket created")

        s.connect(server_addr)
        log("Connected with {}:{}".format(server_addr))

        while True:
            op = get_client_input()

            if op == 0:
                s.close()
                return

            msg = op.encode()
            s.sendall(msg)

            data = s.recv(1024).decode("utf-8")

            print(data)


def udp_with_server(server_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)
        while True:
            op = get_client_input()

            s.sendto(op.encode(), server_addr)
            print_sent(op, server_addr)

            data, addr = s.recvfrom(1024)
            print_received(data, addr)


def get_client_input():

    while True:
        print("1. List files")
        print("0. end connection")

        try:
            possible_ans = [0, 1, 2]
            ans = int(input("  -> "))

            if ans not in possible_ans:
                raise ValueError("some exception here!!")
        except ValueError:
            print("input in the wrong format!")
            continue

        return str(ans)


def log(msg):
    print("--", msg)

def print_received(msg, addr):
    if isinstance(msg, str):
        print("  <- {} from {}".format(msg, addr))
    else:
        print("  <- {} from {}".format(msg.decode("utf-8"), addr))

def print_sent(msg, addr):
    if isinstance(msg, str):
        print("  -> {} to {}".format(msg, addr))
    else:
        print("  -> {} to {}".format(msg.decode("utf-8"), addr))


if __name__ == "__main__":
    main()
