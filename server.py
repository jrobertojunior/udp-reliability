#!/usr/bin/env python3

import socket
import time
import os
from support import *
from random import randint
import select
from udp_confiability import *
import threading

DOMAIN = "www.foo123.org"
THIS_ADDR = ("localhost", 65432)
DNS_ADDR = ('localhost', 65431)

BUF = 1024

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
            op, addr = receive_message(s, print_status=True)

            if op == "1":
                msg = str(os.listdir("./server_data"))
                # s.sendto(msg.encode(), addr)
                send_message(msg, addr, s, print_status=True)
                print_sent(msg, addr)

            # elif op == "2":
                # data, addr = s.recvfrom(BUF)
                # log("server was requested to send " + data.decode("utf-8"))
                # send_file(data.decode("utf-8"), addr, s)

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


def udp_with_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)

        while True:
            data, addr = s.recvfrom(BUF)
            msg_received = data.decode("utf-8")
            print_received(msg_received, addr)

            if msg_received == "1":
                msg = str(os.listdir("./server_data"))
                s.sendto(msg.encode(), addr)
                print_sent(msg, addr)

            elif msg_received == "2":
                data, addr = s.recvfrom(BUF)
                log("server was requested to send " + data.decode("utf-8"))
                send_file(data.decode("utf-8"), addr, s)

            elif msg_received == "0":
                break

    log("end of communication with client")


def get_list_files():
    files = os.listdir("./server_data")

    msg = ""
    i = 1
    for f in files:
        msg += "{}. {}\n".format(i, f)
        i += 1

    return msg


def send_file(filename, addr, sock):
    with open("server_data/" + filename, "rb") as f:
        while True:
            data = f.read(BUF - 1)

            if not data:
                break

            data = bytearray(data)  # bytes are immutable, convert o bytearray
            data.append(1)  # append another byte
            rand_n = randint(0, 255)  # generate random rand_n number
            data[-1] = rand_n  # write hash number

            while True:
                sock.sendto(data, addr)

                received = False
                correct_random = False

                ready = select.select([sock], [], [], timeout)
                if ready[0]:
                    data, addr = sock.recvfrom(BUF)
                    received = True
                else:
                    log("timeout, sending {} again".format(rand_n))

                if int(data.decode("utf-8")) == rand_n:
                    print("ok", data)
                    correct_random = True

                if received and correct_random:
                    break

        log("sent {} to {}".format(filename, addr))


def log(msg):
    print("-", msg)


if __name__ == "__main__":
    main()
