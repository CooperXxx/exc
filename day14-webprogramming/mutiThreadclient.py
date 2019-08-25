from socket import socket
from json import loads
from base64 import b64decode

def main():
    client = socket()
    client.connect(('10.203.150.247', 6789))

    # print(client.recv(1024).decode("utf-8"))
    # client.close()


    in_data = bytes()
    data = client.recv(1024)

    while data:
        in_data += data
        data = client.recv(1024)

    my_dict = loads(in_data.decode("utf-8"))

    filename =  my_dict["filename"]
    filedata = my_dict["filedata"]

    with open("after"+filename,"wb") as f :
        f.write(b64decode(filedata))

    print("photo saved")

if __name__ == '__main__':
    main()