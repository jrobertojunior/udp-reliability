# Projeto DNS Infraestrutura de Comnumicação

```
Este projeto teve como objetivo implmentar uma comunicação cliente-servidor via UDP garantindo confiabilidade. Um servidor-DNS simplificado é responsável por fornecer o endereço do servidor ao cliente, uma vez que ele já tenha previamente recebido o endereço do servidor.

Autor: José Roberto Fonseca e Silva Júnior, jrfsj@cin.ufpe.br
```

## Sumário

- [Projeto DNS Infraestrutura de Comnumicação](#Projeto-DNS-Infraestrutura-de-Comnumica%C3%A7%C3%A3o)
  - [Sumário](#Sum%C3%A1rio)
  - [Módulo DNS](#M%C3%B3dulo-DNS)
    - [Mapeamento de endereços](#Mapeamento-de-endere%C3%A7os)
    - [Inicialização](#Inicializa%C3%A7%C3%A3o)
    - [Loop](#Loop)
      - [Formato geral de uma mensagem](#Formato-geral-de-uma-mensagem)
      - [Mensagem do servidor](#Mensagem-do-servidor)
      - [Mensagem do cliente](#Mensagem-do-cliente)
  - [Módulo servidor](#M%C3%B3dulo-servidor)
    - [Comunicação com servidor DNS](#Comunica%C3%A7%C3%A3o-com-servidor-DNS)
    - [Comunicação com cliente](#Comunica%C3%A7%C3%A3o-com-cliente)
  - [Módulo cliente](#M%C3%B3dulo-cliente)
    - [Inicialização e comunicação com DNS-server](#Inicializa%C3%A7%C3%A3o-e-comunica%C3%A7%C3%A3o-com-DNS-server)
    - [Comunicação com servidor](#Comunica%C3%A7%C3%A3o-com-servidor)
  - [Confiabilidade com UDP](#Confiabilidade-com-UDP)
    - [send_message](#sendmessage)
    - [receive_message](#receivemessage)
  - [Operações cliente-servidor](#Opera%C3%A7%C3%B5es-cliente-servidor)
    - [Listar banco de dados](#Listar-banco-de-dados)
    - [Enviar e receber arquivos](#Enviar-e-receber-arquivos)
    - [Terminar comunicação](#Terminar-comunica%C3%A7%C3%A3o)

Os 4 módulos criados para esse projeto foram:

- dns.py
- server.py
- client.py
- udp_reliability

Seguindo ordem cronológica, a execução e operação desse projeto se dá nos seguintes passos:

1. `dns.py` é executado. Ele fica num loop esperando por mensagens ou do servidor ou do cliente.
2. `server.py` é executado e manda seu domínio e endereço para o servidor DNS.
3. `client.py` é executado. Este fará uma requisição pelo endereço do domínio do server.
4. O cliente com o endereço em mãos, conecta-se com servidor via TCP.
5. Após ter realizado conexão TCP, esta conexão é fechada para, a partir de agora, só se comunicar via UDP com o servidor. Um leque de operações cliente-servidor é apresentado via console ao cliente. As operações são realizadas até que a comunicação seja terminada.

Segundo essa ordem de execução deles é preferível que seja primeiro o `dns`, segundo o `server`, terceiro o `client`.

As seções deste relatório foram divididas em 4:

- Módulo DNS: descreve a implementação do módulo DNS, seja sua comunicação com o cliente ou servidor, assim como o mapeamento dos endereços.
- Módulo servidor: descreve os passos realizados pelo servidos até se comunicar com o cliente.
- Módulo cliente: descreve as operações realizadas pelo cliente e a interface voltada usuário para comunicação cliente-servidor.
- Confiabilidade com UDP: apresenta a abordagem tomada para garantir confiabilidade do transporte de mensagens via UDP.

## Módulo DNS

### Mapeamento de endereços

O trabalho do DNS-server é mapear um nome de domínio para um endereço. Este processo pode ser expresso na estrutura de dados `dict`, do dicionário do Python, pois toma como entrada uma chave e retorar um valor associado a ela. No caso do módulo DNS, a chave é o nome do **domínio** e o valor é o **endereço**. Seja o dicionário de endereços `dns_list`, uma forma de acessar o endereço do site _www.foo123.com_ seria dessa forma:

dns_list["www.foo123.com"] -> ("localhost", 65432)

### Inicialização

Ao ser inicializado, o módulo DNS cria um socket UDP, faz um bind no endereço **(localhost, 65431)**, oculto no macro **THIS_ADDR** e conhecido pelo cliente e sevidor.

```python
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  # creating UDP socket
    print("DNS socket created")

    s.bind(THIS_ADDR)  # bind to ("localhost", 65431)
```

### Loop

Usando o socket criado, o DNS-server entra num **loop eterno** enquanto aberto para receber mensagens.

#### Formato geral de uma mensagem

Uma mensagem recebida vem na forma `source;{};{};{}`, onde cada componente vem separado por ponto e vírgula (`;`).

- `source`: Indica quem é a fonte da mensagem. Pode ser ou `client` ou `server`, indicando que a mensagem vem do cliente ou do servidor, respectivamente.
- `{}`: Campos opcionais. Varia com o propósito de cada mensagem.

```python
while True:
    data, addr = s.recvfrom(BUF)  # wait for data to receive
    msg = data.decode("utf-8").split(';')  # message handling
```

O DNS é preparado para receber dois tipos de mensagens, sendo uma delas vinda do servidor e outra vindo do cliente.

#### Mensagem do servidor

O servidor só se comunica com o DNS-server para mandar seu domínio e endereço, então se a mensagem recebida vier de um servidor, os campos opcionais `{}` virão na forma `{domain_name};{host};{port}`. Assim o DNS-server atualiza dicionário de relações com uma nova entrada.

```python
if msg[0] == "server":
    key, value = (msg[1], (msg[2], msg[3]))
    dns_list[key] = value  # update dns dictionary
```

#### Mensagem do cliente

O cliente só se comunica com o DNS-server para requisitar um endereço baseado num nome de domínio. Então se a mensagem vier de um servidor, o módulo DNS checa se existe uma entrada no seu `dns_list` com esse nome. Se sim, ele retorna o valor associado (endereço), senão, retorna `"null"`.

```python
elif msg[0] == "client":
    key = msg[1]

    if key in dns_list:
        reply = str(dns_list[key]).encode()
        s.sendto(reply, addr)  # reply client with server addres
    else:
        s.sendto("null".encode(), addr)  # domain name not in dict. Reply null to client
```

## Módulo servidor

Esta seção descreve as operações realizadas pelo servidor, que podem ser dividias em duas: **comunicação com servidor DNS** e **comunicação com cliente**.

### Comunicação com servidor DNS

A primeira operação que o servidor realiza é mandar seu domínio e endereço para o servidor DNS via UDP.

```python
def main():
    send_address_to_dns(DOMAIN, DNS_ADDR)

[...]

def send_address_to_dns(server_dns, dns_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # building message
        # "www.foo123.com;localhost;65432"
        msg = "server;{};{};{}".format(server_dns, THIS_ADDR[0], THIS_ADDR[1]).encode()

        s.sendto(msg, DNS_ADDR)  # sending message to DNS-server
```

### Comunicação com cliente

Após ter mandando seu endereço para o módulo DNS, é esperado que o cliente se comunique com o servidor. Para isso, o servidor cria um socket UDP associado com o mesmo endereço que foi mandado para o DNS-server.

```python
def udp_with_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)

        while True:
            data, addr = s.recvfrom(BUF)
            msg_received = data.decode("utf-8")

            if msg_received == "1":  # client requested list of files
                msg = str(os.listdir("./server_data"))  # list of files in ./server_data
                s.sendto(msg.encode(), addr)  # send list to client

            elif msg_received == "2":  # client requested a file
                data, addr = s.recvfrom(BUF)
                send_file(data.decode("utf-8"), addr, s)

            elif msg_received == "0":  # client stopped communication
                break
```

Dentro do loop, o server age de acordo com a operação que o cliente deseja fazer. No total são 3 operações, e suas descrições estão seção _Módulo cliente_ e _Garantindo confiabilidade_.

## Módulo cliente

### Inicialização e comunicação com DNS-server

Para se comunicar com o servidor, o cliente primeiramente faz uma requisição ao servidor DNS pelo endereço de um certo domínio. Assim, primeiro comando executado pelo cliente é a chamada da função `ask_address_to_dns` que trata essa comunicação com o DNS-server.

```python
def ask_address_to_dns(domain):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(THIS_ADDR)

        msg = "client;{}".format(domain).encode()  # message building
                                                   # "client;www.foo123.com"

        s.sendto(msg, DNS_ADDR)  # send dns request message

        data, addr = s.recvfrom(BUF)  # await for response

        return handle_dns_message(data)
```

A função exposta acima retorna o endereço do servidor. _OBS Está oculta a função `handle_message` para simplificar a explicação, mas o que ela faz é basicamente tratamento de string._

### Comunicação com servidor

Num primeiro momento, o cliente-servidor estabelecem uma conexão TCP. Depois, trocam mensagens apenas via UDP.

Um socket UDP é criado e associado ao endereço do servidor.

```python
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(THIS_ADDR)
```

Depois, este socket é usado num loop infinito que perdura até que o cliente deseje encerrar a comunicação.

```python
while True:
    data, addr = s.recvfrom(BUF)
    msg_received = data.decode("utf-8")
```

Dentro do loop, a função `get_user_input` dispôe para o usuário 3 opções de ação:

1. End communication. Esta ação interrompe o andamento tando do loop após mandar uma mensagem para o servidor com o conteúdo _"**0**"_, indicando para ele também interromper seu loop.
2. List files. Envia uma mensagem _"**1**"_ ao servidor requisitando uma lista dos arquivos no banco de dados.
3. Request file. Primeiro, envia uma mensagem ao servidor com o número da operação (_"**2**"_), que, por sua vez, espera por outra mensagem. Essa segunda mensagem que vem do cliente contém o _filename_. Então, o cliente executa a função `receive_file`, que recebe um arquivo usando funções que abstraem para o cliente a implementação da confiabilidade do UDP. \*As funções de confiabilidade estão descritas na seção **_Garantindo confiabilidade_\***

## Confiabilidade com UDP

A confiabilidade do UDP foi implementada na operação em que o servidor envia um arquivo para o cliente. São duas funções que tratam de todo o processo: `send_message` e `receive message`.

Antes de entrar em código, é interessante explicar a lógica utilizada para garantir essa confiabilidade.

Basicamente, quem envia um _packet_ usa o último byte da sequência para guardar um número chamado `h` - um número baseado num **hash** que tem como entrada a sequência de bytes do pacote, ou seja, se a seência for diferente, muito provavelmente o hash também vai dar. Como apenas um byte foi reservado, este número vai de 0 a 255.

Entende-se que se o cliente recebeu o packet de forma confiável, o último byte é igual ao último byte do packet que saiu do servidor, análogo ao número de segmento.

1. O server manda uma packet com dados + `h`.
2. Se o cliente recebeu o packet, ele retorna uma mensagem com `h`
3. Se o server recebe o `h` do cliente, ele compara com o `h` local.
   1. Se os números forem iguais, o server retorna **1** para o cliente.
   2. Senâo, o server retorna **0**.

Todos os passos reportados acima são executados dentro um intervalo de tempo chamado `timeout`. Caso algum passo não se encaixe nessa janela, tudo é repetido, evitando que aconteça uma espera eterna.

### send_message

A função `send_message` recebe 3 parâmetros:

1. `msg`: os bytes da mensagem.
2. `addr`: o endereço de destino.
3. `sock`: o socket usado.

Primeiramente, é concateado o array de bytes `msg` com o hash `h` desse vetor.

```python
msg, h = append_hash(msg)  # length of msg + h 1024 bytes
```

Envia-se via UDP a mensagem com o hash, depois, espera-se por uma resposta `ack` do cliente.

```python
ack, addr = sock.recvfrom(1023)  # wait for client ack

if ack == h:  # correct ack
    sock.sendto("1".encode(), addr)  # tell the client it's ok
    return 1
else:  # wrong ack
    sock.sendto("0".encode(), addr)  # tell the client that hash doesn't match
```

Se o `ack`, que é o hash do cliente, for igual ao `h`, o hash local, o servidor envia **1**, senão, **0**.

### receive_message

Para toda send_message, existe uma receive_message. Esta função age como complemento.

Primeiro, compara-se o `h` da mensagem com o o `h` local. Sendo ambos iguais, envia-se esse `h` como resposta e espera-se por um `ack` do remetente, que se for **1**, ocorreu tudo ok. Senão, o _loop_ roda novamente.

```python
while True:
    data, addr = sock.recvfrom(1024)  # receive data

    received_hash = str(data[-1])  # get ack

    if received_hash == get_hash(data):  # correct hash
        sock.sendto(received_hash.encode(), addr)  # send ack

        server_ack, addr = sock.recvfrom(1024)  # wait for server ack

        if server_ack == "1":
            return data, addr  # return data
    else:
        time.sleep(TIMEOUT)
```

Como percebe-se acima, caso o hash recebido com o calculado forem diferentes, espera-se o TIMEOUT, que é o tempo necessário para o server mandar novamente os dados.

## Operações cliente-servidor

### Listar banco de dados

Quando o servidor recebe **1** do cliente, ele retorna uma lista com todos os arquivos contidos dentro do diretório `server_data`, e envia para o cliente usando a função já descrita `send_message` que implementa confiabilidade UDP.

```python
if op == "1":
    msg = str(os.listdir("./server_data"))
    send_message(msg, addr, s)
```

O cliente recebe essa mensagem e a dispôe no console:

```python
if op == "1":
    data, addr = receive_message
```

### Enviar e receber arquivos

Estão implementadas em `receive_file`, para o cliente, e `send_file`, para o servidor.

No lado do cliente, a requisição é feita usando o código **2**, e em seguida, o nome do arquivo. Quando servidor recebe esse código, prepara-se para receber o nome do arquivo em sequência.

As funções `send_file` recebe 3 parâmetros:

1. `filename`: o nome do arquivo
2. `addr`: o endereço destino
3. `sock`: o socket usado

No início, a função abre o arquivo no seu banco de dados, que está contido no diretório `server_data`. Depois, vai lendo pedaços de **1023 bytes** (o motivo é explicado na seção de confiabilidade UDP) até que não haja mais o que ler.

```python
with open("server_data/" + filename, "rb") as f:
    while True:
        data = f.read(1023)

        if not data:
            break

        send_message(data, addr, sock)
```

No lado do cliente, ele recebe os arquivos em sequência até que um tempo `timeout` ocorra sem receber arquivos. Usou-se a biblioteca `select` para implementar o desbloqueio da função `socket.recvfrom()`, impedindo que o cliente esperasse para sempre por um aquivo.

```python
def receive_file(filename, sock):
    with open("client_data/" + filename, 'wb') as f:
        begin = time.process_time()

        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                data, addr = receive_message(sock)
                f.write(data)
            else:
                f.close()
                break
```

### Terminar comunicação

Quando o cliente escolhe a operação **0**, ele envia esse valor para o servidor. Ambos usam o comando `break` para sair do loop que encapsula o socket.

```python
if op == "0":
    break
```
