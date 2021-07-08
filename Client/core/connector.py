import json
import socket
import hashlib
import rsa


class Connector:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.5)
        self.server_ip = 'localhost'
        self.port = 2137
        self.login = ''
        self.token = -1
        self.server_public_key = None
        self.my_public_key = None
        self.my_private_key = None
        (self.my_public_key, self.my_private_key) = rsa.newkeys(2048)
        self.get_server_public_key()
        print(self.server_public_key)

    def get_server_public_key(self):
        public_key = self.send_message_to_server({'command': 'get_public_key',
                                                  'client_public_key': [self.my_public_key.n,
                                                                        self.my_public_key.e]})['public_key']
        self.server_public_key = rsa.PublicKey(public_key[0], public_key[1])

    def set_token(self, _token):
        self.token = _token

    def send_message_to_server(self, data_to_send):

        if self.server_public_key is None:
            self.sock.sendto(json.dumps(data_to_send).encode('utf-8'), (self.server_ip, self.port))
        else:
            try:
                self.sock.sendto(rsa.encrypt(json.dumps(data_to_send).encode('utf-8'), self.server_public_key),
                                (self.server_ip, self.port))
            except:
                self.sock.sendto(json.dumps(data_to_send).encode('utf-8'), (self.server_ip, self.port))
        try:
            data, address = self.sock.recvfrom(1024)
        except:
            return self.send_message_to_server(data_to_send)
        if self.server_public_key is None:
            print('t')
            return json.loads(data.decode('utf-8'))
        else:
            print('a')
            try:
                return json.loads(rsa.decrypt(data, self.my_private_key).decode('utf-8'))
            except:
                return json.loads(data.decode('utf-8'))

    def log_in(self, login, password):
        return self.send_message_to_server({
            "command": "login",
            "login": login,
            "password": hashlib.sha512(password.encode()).hexdigest()
        })

    def registration(self, login, password, email):
        return self.send_message_to_server({
            "command": "registration",
            "login": login,
            "password": hashlib.sha512(password.encode()).hexdigest(),
            "email": email
        })

    def log_out(self):
        return self.send_message_to_server({
            "command": "logout",
            "login": self.login,
            "token": self.token
        })

    def get_list_of_friends(self):
        return self.send_message_to_server({
            "command": "get_list_of_friends",
            "login": self.login,
            "token": self.token
        })

    def forgot_password(self, login):
        return self.send_message_to_server({
            "command": "forgot_password",
            "login": login
        })

    def change_password(self, login, code, new_password):
        return self.send_message_to_server({
            "command": "change_password",
            "login": login,
            "code": code,
            "new_password": new_password
        })

    def delete_friend(self, friend_login):
        return self.send_message_to_server({
            "command": "remove_friend",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login
        })

    def invite_friend(self, friend_login):
        return self.send_message_to_server({
            "command": "invite_friend",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login
        })

    def get_message(self):
        return self.send_message_to_server({
            "command": "get_message",
            "login": self.login,
            "token": self.token
        })

    def accept_invite(self, friend_login):
        return self.send_message_to_server({
            "command": "accept_invite",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login
        })

    def send_message_to_friend(self, friend_login, message):
        return self.send_message_to_server({
            "command": "send_message_to_friend",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login,
            'message': message
        })
