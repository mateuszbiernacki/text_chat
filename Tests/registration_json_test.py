import socket
import json

JSON_DATA = {
    "command": "registration",
    "login": "L'Hospital",
    "password": "2137",
    "email": "testowe@email"
}

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(JSON_DATA).encode(), ("localhost", 2137))
    data, address = sock.recvfrom(1024)
    print(data)
