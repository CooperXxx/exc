from socket import socket, SOCK_STREAM, AF_INET
from datetime import datetime


def main():
    server = socket(type=SOCK_STREAM,family=AF_INET)
    server.bind(('10.203.150.247', 6789))
    server.listen(512)

    print("server start to listen:")

    while True:

        client,addr=server.accept()
        print(str(addr)+"connect on server")
        client.send(str("good good good").encode("utf-8"))
        client.close()


if __name__ == '__main__':
    main()