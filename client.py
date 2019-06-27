#!/usr/bin/env python3

import socket
from support import *
import select
import time
import random

timeout = 3
database = {}

DNS_ADDR = ('localhost', 65431)
THIS_ADDR = ("localhost", 65430)

BUF = 1024

fake_error = True


def main():
    # domain = input("Type the domain to get address\n-> ")
    addr = ask_address_to_dns("www.foo123.org")

    log("client will start conversation with server")
    udp_with_server(addr)


def ask_address_to_dns(domain):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)

        msg = "client;{}".format(domain).encode()

        s.sendto(msg, DNS_ADDR)  # send dns request message
        print_sent(msg, DNS_ADDR)

        data, addr = s.recvfrom(BUF)
        print_received(data, addr)

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
            op = get_user_input()

            if op == 0:
                s.close()
                return

            msg = op.encode()
            s.sendall(msg)

            data = s.recv(BUF).decode("utf-8")

            print(data)


def udp_with_server(server_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)
        while True:
            op = get_user_input()

            s.sendto(op.encode(), server_addr)
            print_sent(op, server_addr)

            if op == "0":
                break
            elif op == "1":
                data, addr = s.recvfrom(BUF)
                print_received(data, addr)
            elif op == "2":
                filename = input("type filename\n-> ")
                s.sendto(filename.encode(), server_addr)
                receive_file(filename, s)

    log("end of communication with server")


def get_user_input():

    while True:
        print("\n----- MENU -----")
        print("0. End communication")
        print("1. List files")
        print("2. Request file")

        try:
            possible_ans = [0, 1, 2]
            ans = int(input("-> "))

            if ans not in possible_ans:
                raise ValueError("some exception here!!")
        except ValueError:
            print("input in the wrong format!")
            continue

        return str(ans)


def receive_file(filename, sock):
    with open("client_data/" + filename, 'wb') as f:
        begin = time.process_time()

        while True:
            if fake_error and random.randint(0, 9) % 9 != 0:
                data, addr = sock.recvfrom(BUF)
                sock.sendto(str(data[-1] + 1).encode(), addr)

            else:
                ready = select.select([sock], [], [], timeout)
                if ready[0]:
                    data, addr = sock.recvfrom(BUF)
                    print(data[-1], addr)
                    f.write(data[:-1])
                    sock.sendto(str(data[-1]).encode(), addr)
                else:
                    log("TIMEOUT")
                    f.close()
                    break

    log("file transfer took {} seconds".format(
        time.process_time() - begin - timeout))


if __name__ == "__main__":
    main()
