#!/usr/bin/env python3

import socket
import time
from threading import Thread

addresses = {}


def main():

    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65431        # DNS port that I use in this project

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("DNS socket created")

        s.bind((HOST, PORT))
        s.listen()

        print("Now listening")

        while True:
            connection, address = s.accept()
            ip, port = address[0], address[1]
            print("Connected with {}:{}".format(ip, port))

            Thread(target=client_thread, args=[connection, ip, port]).start()


# this thread handles the communication with the client
# a client could be a server uploading its address a client requesting it
def client_thread(connection, ip, port):
    while True:
        data = connection.recv(1024).decode("utf-8").split(';')

        if data[0] == "server":
            key, value = (data[1], (data[2], data[3]))
            addresses[key] = value

            print("  received")
            print("  -> {{{}}}: {{{}}}".format(key, value))

            connection.close()
            break

        elif data[0] == "client":
            key = data[1]

            msg = None

            if key in addresses:
                msg = str(addresses[key]).encode()
            else:
                msg = "null".encode()

            connection.sendto(msg, (ip, port))
            # msg = str(addresses[data[1]]).encode()

            print("  sent")
            print("  ->", msg.decode())

            connection.close()
            break

    print("Connection with {}:{} closed".format(ip, port))


if __name__ == "__main__":
    main()
