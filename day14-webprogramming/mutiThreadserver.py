from threading import Thread
from socket import socket,SOCK_STREAM,AF_INET
from json import dumps
from base64 import b64encode

def main():

    class FileTransferHandler(Thread):

        def __init__(self,cclient):
            super().__init__()
            self._cclient = cclient

        def run(self):
            my_dict={}
            my_dict['filename']="243.jpg"
            my_dict["filedata"]=data
            json_str = dumps(my_dict)


            # encode 才是编码成二进制
            # decode 是解码成str
            # 这里要注意和b64decode和b64encode的区别
            self._cclient.send(json_str.encode("utf-8"))
            print(type(json_str.encode("utf-8")))
            self._cclient.close()

    server = socket(type=SOCK_STREAM, family=AF_INET)
    server.bind(('10.203.150.247', 6789))
    server.listen(512)

    print("server start to listen:")

    with open("253.jpg","rb") as f:
        # base64 编码是编码，不是转换成二进制数据，所以这里data是str
        data = b64encode(f.read()).decode("utf-8")
        # print(type(data))
        # data = f.read()
        # print(type(data))
    while True:
        client, addr = server.accept()
        print(str(addr) + "connect on server")
        FileTransferHandler(client).start()


if __name__ == '__main__':
    main()