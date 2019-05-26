#!/usr/bin/env python3

import socket
import time

addresses = {}


def main():

    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65431        # DNS port that I use in this project

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()

            with conn:
                print('Connected by', addr)

                begin = time.perf_counter()

                while True:
                    data = conn.recv(1024).decode("utf-8")

                    if data:
                        print("\t<-", data)

                        data = data.split(';')

                        if data[0] == "server":

                            # end connection
                            if data[1] == "bye":
                                break

                            # add to adresses dicionary
                            else:
                                addresses[data[1]] = data[2]
                                print(addresses)
                                s.sendall("ok".encode())

                        elif data[0] == "client":
                            print("FALANDO COM CLIENTE!")

                        begin = time.perf_counter()

                    elif time.perf_counter() - begin > 3:
                        print("waiting for data...")
                        begin = time.perf_counter()


if __name__ == "__main__":
    main()
