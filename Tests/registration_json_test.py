import socket
import json
import time

import rsa

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    (public_key, private_key) = rsa.newkeys(1024)

    JSON_DATA = {
        "command": "get_public_key",
        "client_public_key": [public_key.n, public_key.e],
    }

    sock.sendto(json.dumps(JSON_DATA).encode(), ("localhost", 2137))
    data, address = sock.recvfrom(1024)
    server_key = rsa.PublicKey(json.loads(data)['public_key'][0], json.loads(data)['public_key'][1])

    print(data)

    for i in range(1000):
        JSON_DATA = {
            "command": "registration",
            "login": f"matefduuuhhsusdz{i}",
            "password": "213",
            "email": f"tesddfthhow{i}e@email"
        }

        sock.sendto(json.dumps(JSON_DATA).encode(), ("localhost", 2137))
        print('done')
