import socket
from random import randint
import select
from support import *
import time

# BUF = 1023


def send_message(msg, addr, sock, print_status=False):
    if isinstance(msg, str):
        msg = msg.encode()

    msg, rand_n = append_rand_n(msg)  # len 1024

    while True:
        sock.sendto(msg, addr)  # send message to client
        if print_status:
            print_sent(msg, addr)

        ack, addr = sock.recvfrom(1023)  # wait for client ack

        ack = int(ack.decode("utf-8"))
        if ack == rand_n:
            if print_status:
                print("correct ack, {} = {}".format(ack, rand_n))

            sock.sendto("1".encode(), addr)  # tell the client it's ok
            return 1
        else:
            if print_status:
                print("wrong ack! {} != {}".format(ack, rand_n))

            sock.sendto("0".encode(), addr)  # tell the client it isn't ok
            time.sleep(0.5)


def receive_message(sock, print_status=False):
    while True:
        data, addr = sock.recvfrom(1024)
        if print_status:
            print_received(data, addr)

        client_ack = str(data[-1])  # get ack

        sock.sendto(client_ack.encode(), addr)  # send ack
        if print_status:
            print_sent(client_ack, addr)

        server_ack, addr = sock.recvfrom(1024)
        if print_status:
            print_received(server_ack, addr)
        server_ack = server_ack.decode("utf-8")

        if server_ack == "1":
            try:
                return data[:-1].decode("utf-8"), addr
            except UnicodeDecodeError:
                return data[:-1], addr

        if print_status:
            print("incorrect ack...")


def append_rand_n(data):
    # rand_n = randint(0, 10)  # generating random number
    h = get_hash(data)

    # return data + bytes([rand_n]), rand_n
    return data + bytes([h]), h


def get_hash(data):
    s = str(hash(data))

    if s[0] == '-':
        s = s[1:]

    total = 0
    for c in s:
        total += int(c)

    return total
