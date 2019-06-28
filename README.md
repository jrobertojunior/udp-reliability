# UDP with reliability

## What is

> This project was made to Communication Infrastructure course, Center of Informatics - Federal University of Pernambuco.

The main purpose of this project is to establish a client-server communication using UDP (User Datagram Protocol) while guaranteeing **reliability**. To test this reliability, a file transfer operation was implemented.

Another feature is the implementation of a simple DNS server. Initially, the client doesn't know the server address. Only after requesting the DNS-server, the client reaches the server to start communication.

This project is fully implemented in **Python 3.7** and `socket` library. The files were separated into four modules:

- [dns.py](dns.py) - Implements DNS-server.
- [server.py](server.py) - Server that will communicate with the client.
- [client.py](client.py) - Client that will communicate with the server.
- [**udp_reliability.py**](udp_reliability.py) - Module that holds a set of functions that implements sending and receiving messages via UDP with reliability.


## Why

### UDP vs TCP

In contrast with TCP, UDP is a connectionless protocol that doesn't guarantee to the source if the message has arrived at the destination, one of which reasons is the lack of the ***ack*** (acknowledgment) field.

This project aims to implement client-server *ack* of packet arrival using UDP to guarantee a certain level of reliability.

### DNS module

The simplified DNS-server simulates on many occasions what happens in practice on the internet: the client doesn't know the server address before it requests to the DNS-server with a **domain name**.

## How to use

Execute the following commands within independent consoles:

1. \$ `python dns.py`.
2. \$ `python server.py`.
3. \$ `python client.py`.

After launching the client, it should lead to user input, presenting a set of client-server interactions.

If you choose to transfer a file, be sure that the server has the file in the directory `server_data`. If it has, it will be downloaded to the `client_data` directory.

## Current status

The *ack* guarantees that the user has received the file without being corrupted. However, if one of the messages aren't delivered in the whole process, one of the modules (client or server) will keep waiting for it. This is caused because it's not implemented a ***timeout interruption***. Basically, what it does is to send another message if the source hasn't received a reply within the timeout interval. This is intended to be implemented further.

## Contribution

If you want to contribute with this project, you can start by implementing the *timeout interruption*.

## Author

**J. Roberto Fonseca Jr.**, undergraduate in computer engineering at CIn-UFPE.

## Other

This project accompanies a report [Relatorio.md](Relatorio.md) that is written in Portuguese. It describes most of the functions used.

***Contact**: jrfsj@cin.ufpe.br*
