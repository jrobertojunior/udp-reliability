#!/usr/bin/env python3

import socket
import time
import os
from support import *
from random import randint
import select
from udp_reliability import *
import threading

DOMAIN = "www.foo123.org"
THIS_ADDR = ("localhost", 65432)
DNS_ADDR = ('localhost', 65431)

BUF = 1023

timeout = 1


def main():
    send_address_to_dns(DOMAIN, DNS_ADDR)
    log("sent addres to DNS with success")

    tcp_with_client()
    log("established TCP conn with client with success")

    # time.sleep(2)

    new_udp_with_client()
    log("end of program")


def new_udp_with_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)

        while True:
            op, addr = receive_message(s, print_status=False)

            if op == "1":
                msg = str(os.listdir("./server_data"))
                send_message(msg, addr, s, print_status=False)
                print_sent(msg, addr)

            elif op == "2":
                filename, addr = receive_message(s, print_status=True)
                send_file(filename, addr, s)

            elif op == "0":
                break

            # result = send_message(msg, addr, s, print_status=False)


def send_address_to_dns(server_dns, dns_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        msg = "server;{};{};{}".format(
            server_dns, THIS_ADDR[0], THIS_ADDR[1]).encode()
        s.sendto(msg, DNS_ADDR)

        print("  -> {} to {}".format(msg.decode("utf-8"), DNS_ADDR))


def tcp_with_client():
    addr = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(THIS_ADDR)
        s.listen()
        conn, addr = s.accept()

        with conn:
            log("connected with {}".format(addr))

    return addr


def get_list_files():
    files = os.listdir("./server_data")

    msg = ""
    i = 1
    for f in files:
        msg += "{}. {}\n".format(i, f)
        i += 1

    return msg


def send_file(filename, addr, sock):
    try:
        with open("server_data/" + filename, "rb") as f:
            send_message("1", addr, sock)
            time.sleep(2)
            while True:
                data = f.read(1023)

                if not data:
                    break

                send_message(data, addr, sock)
    except FileNotFoundError:
        print("file not found!")
        send_message("-1", addr, sock)


def log(msg):
    print("-", msg)


if __name__ == "__main__":
    main()
