# Projeto DNS lógica

*Autor: José Roberto Fonseca e Silva Júnior, jrfsj@cin.ufpe.br*

Este projeto teve como objetivo implmentar uma comunicação cliente-servidor via UDP garantindo confiabilidade. Um servidor-DNS simplificado deve ser responsável por fornecer o endereço do servidor ao cliente, uma vez que ele já tenha previamente recebido o endereço do servidor.

A divisão dos programas ocorreu em 3 módulos.

* dns.py
* server.py
* client.py

## Módulo DNS

### Mapeamento de endereços

O trabalho do DNS-server é mapear um nome de domínio para um endereço. Este processo pode ser expresso na estrutura de dados `dict`, do dicionário do Python, pois toma como entrada uma chave e retorar um valor associado a ela. No caso do módulo DNS, a chave é o nome do **domínio** e o valor é o **endereço**. Seja o dicionário de endereços `dns_list`, uma forma de acessar o endereço do site *www.foo123.com* seria dessa forma:

dns_list["www.foo123.com"] -> ("localhost", 65432)

### Inicialização

Ao ser inicializado, o módulo DNS cria um socket UDP, faz um bind no endereço **(localhost, 65431)**, que é conhecido pelo cliente e sevidor.

```python
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  # creating UDP socket
    print("DNS socket created")

    s.bind(THIS_ADDR)  # bind to ("localhost", 65431)
```

### Loop

Usando o socket criado, o DNS-server entra num **loop eterno** enquanto aberto para receber mensagens.

#### Formato geral de uma mensagem

Uma mensagem recebida vem na forma `source;{};{};{}`, onde cada componente vem separado por ponto e vírgula (`;`).


* `source`: Indica quem é a fonte da mensagem. Pode ser ou `client` ou `server`, indicando que a mensagem vem do cliente ou do servidor, respectivamente.
* `{}`: Campos opcionais. Varia com o propósito de cada mensagem.

``` python
while True:
    data, addr = s.recvfrom(BUF)  # wait for data to receive
    msg = data.decode("utf-8").split(';')  # message handling
```

O DNS é preparado para receber dois tipos de mensagens, sendo uma delas vinda do servidor e outra vindo do cliente.

#### Mensagem do servidor

O servidor só se comunica com o DNS-server para mandar seu domínio e endereço, então se a mensagem recebida vier de um servidor, os campos opcionais `{}` virão na forma `{domain_name};{host};{port}`. Assim o DNS-server atualiza dicionário de relações com uma nova entrada.

``` python
if msg[0] == "server":
    key, value = (msg[1], (msg[2], msg[3]))
    dns_list[key] = value  # update dns dictionary
```

#### Mensagem do cliente

O cliente só se comunica com o DNS-server para requisitar um endereço baseado num nome de domínio. Então se a mensagem vier de um servidor, o módulo DNS checa se existe uma entrada no seu `dns_list` com esse nome. Se sim, ele retorna o valor associado (endereço), senão, retorna `"null"`.


``` python
elif msg[0] == "client":
    key = msg[1]

    if key in dns_list:
        reply = str(dns_list[key]).encode()
        s.sendto(reply, addr)  # reply client with server addres
    else:
        s.sendto("null".encode(), addr)  # domain name not in dict. Reply null to client

```