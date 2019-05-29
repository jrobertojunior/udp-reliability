#!/usr/bin/env python3

import socket
import time
from threading import Thread

addresses = {}


def main():

    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65431        # DNS port that I use in this project

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            connection, address = s.accept()
            ip, port = address[0], address[1]
            print("Connected with {}:{}".format(ip, port))

            Thread(target=client_thread, args=[
                   connection, s, ip, port]).start()


def client_thread(connection, socket, ip, port):
    while True:
        data = connection.recv(1024).decode("utf-8").split(';')

        if data[0] == "server":
            key, value = (data[1], data[2])
            addresses[key] = value

            print("ADD TO DIC: {{{}}}: {{{}}}".format(key, value))
            break

        # elif data[0] == "client":
        #     msg = str(addresses[data[1]]).encode()
        #     socket.sendto(msg, (ip, port))


if __name__ == "__main__":
    main()
