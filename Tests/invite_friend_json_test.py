import socket
import json

JSON_DATA = {
    "command": "invite_friend",
    "login": "testowy_login",
    "token": "testowe_haslo",
    "friend_login": "testowy_login_kolegi"
}

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(JSON_DATA).encode(), ("localhost", 2137))