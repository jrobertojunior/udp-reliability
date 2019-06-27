#!/usr/bin/env python3

import socket
import time
from threading import Thread
from support import *

dns_list = {}

THIS_ADDR = ("localhost", 65431)

BUF = 1024


def main():
    i = 1

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)
        log("DNS socket setted up at {}".format(THIS_ADDR))

        while True:
            data, addr = s.recvfrom(BUF)  # wait for data to receive
            msg = data.decode("utf-8").split(';')
            print_received(msg, addr)
            # print("  <- {} from {}".format(msg, addr))

            if msg[0] == "server":
                key, value = (msg[1], (msg[2], msg[3]))
                dns_list[key] = value  # update dns dictionary

            elif msg[0] == "client":
                key = msg[1]

                reply = None

                if key in dns_list:
                    reply = str(dns_list[key]).encode()
                else:
                    reply = "null".encode()

                s.sendto(reply, addr)
                print_sent(reply, addr)
                # print("  -> {} to {}".format(reply.decode("utf-8"), addr))


# this thread handles the communication with the client
# a client could be a server uploading its address a client requesting it
def client_thread(conn, ip, port):
    while True:
        data = conn.recv(BUF).decode("utf-8").split(';')

        if data[0] == "server":
            print("  it's a client")
            key, value = (data[1], (data[2], data[3]))
            dns_list[key] = value

            print("  received")
            print("  <- {{{}}}: {{{}}}".format(key, value))

            conn.close()
            break

        elif data[0] == "client":
            print(" it's a server")
            key = data[1]

            msg = None

            if key in dns_list:
                msg = str(dns_list[key]).encode()
            else:
                msg = "null".encode()

            conn.sendto(msg, (ip, port))
            # msg = str(dns_list[data[1]]).encode()

            print("  sent")
            print("  ->", msg.decode())

            conn.close()
            break

    print("Connection with {}:{} closed".format(ip, port))
    print("----------")


if __name__ == "__main__":
    main()
