#!/usr/bin/env python3

import socket
from support import *
import select
import time
import random
from udp_reliability import *
import sys


timeout = 3
database = {}

DNS_ADDR = ('localhost', 65431)
THIS_ADDR = ("localhost", 65433)

BUF = 1024

fake_error = True


def main():
    # domain = input("Type the domain to get address\n-> ")
    addr = ask_address_to_dns("www.foo123.org")
    log("received addres from dns with success")

    tcp_with_server(addr)
    log("established TCP conn with server with success")

    time.sleep(0.5)

    new_udp_with_server(addr)
    log("end of program")


def new_udp_with_server(addr):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)

        while True:
            op = get_user_input()

            send_message(op, addr, s, print_status=False)

            if op == "0":
                break
            elif op == "1":
                data, addr = receive_message(s, print_status=False)
                print_received(data, addr)
            elif op == "2":
                filename = input("type filename\n-> ")
                send_message(filename, addr, s, print_status=False)
                data, addr = receive_message(s)

                if data == "-1":
                    print("file not found!")
                else:
                    receive_file(filename, s)

                # send_message(msg, addr, s, print_status=False)

                # msg, addr = receive_message(s, print_status=False)


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


def tcp_with_server(addr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(addr)
        log("Connected with {}".format(addr))


def get_user_input():

    while True:
        print("\n----- MENU -----")
        print("0. End communication")
        print("1. List files")
        print("2. Request file")

        try:
            possible_ans = [0, 1, 2]
            ans = int(input("-> "))
            sys.stdout.flush()

            if ans not in possible_ans:
                raise ValueError("some exception here!!")
        except ValueError:
            print("input in the wrong format!")
            continue

        return str(ans)


def receive_file(filename, sock):
    with open("client_data/" + filename, 'wb') as f:

        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                data, addr = receive_message(sock)
                try:
                    f.write(data.encode())
                except AttributeError:
                    f.write(data)
            else:
                f.close()
                break


if __name__ == "__main__":
    main()
