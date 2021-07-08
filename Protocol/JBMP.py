"""This is the implementation of JSON Based Messaging Protocol [JBMP]."""
import abc
import json

VERSION = b"1"
ENCODE = "utf-8"


# Message types list:
SERVER_RESPONSE = 'server_response'


class JBMPMessage:
    def __init__(self, message_type, data):
        self.version = VERSION
        self.message_type = message_type
        self.encode = ENCODE
        self.data = data

    def get_message(self):
        import json
        return json.dumps(self.data).encode(self.encode)


class JBMPServerResponseMessageMaker:

    @staticmethod
    def OK_response(long: str):
        return JBMPMessage(SERVER_RESPONSE, {'short': 'OK', 'long': long}).get_message()

    @staticmethod
    def success_login_response(token, address):
        return JBMPMessage(SERVER_RESPONSE, {'short': 'OK',
                                             'long': "Successfully logged.",
                                             'token': token,
                                             'address': address}).get_message()

    @staticmethod
    def get_list_of_friends_response(list_of_friend: list):
        return JBMPMessage(SERVER_RESPONSE, {'short': 'OK',
                                             'list_of_friends': list_of_friend}).get_message()

    @staticmethod
    def get_public_key_response(public_key):
        return json.dumps({'short': 'pubkey', 'public_key': public_key}).encode(ENCODE)

    @staticmethod
    def ERROR_response(long: str):
        return JBMPMessage(SERVER_RESPONSE, {'short': 'Error', 'long': long}).get_message()

    @staticmethod
    def wrong_token_response():
        return JBMPServerResponseMessageMaker.ERROR_response('Wrong token.')

    @staticmethod
    def not_existing_login_response():
        return JBMPServerResponseMessageMaker.ERROR_response('User is not existed.')

    @staticmethod
    def bad_password_response():
        return JBMPServerResponseMessageMaker.ERROR_response('Bad password.')

    @staticmethod
    def occupied_login_response():
        return JBMPServerResponseMessageMaker.ERROR_response('Login is occupied.')

    @staticmethod
    def not_existing_friend_login_response():
        return JBMPServerResponseMessageMaker.ERROR_response('Friend is not existed.')

    @staticmethod
    def not_your_friend_response():
        return JBMPServerResponseMessageMaker.ERROR_response('This user is not in your friends list.')

    @staticmethod
    def not_generated_code_response():
        return JBMPServerResponseMessageMaker.ERROR_response('Code was not generated.')

    @staticmethod
    def bad_code_response():
        return JBMPServerResponseMessageMaker.ERROR_response('Code is wrong.')

    @staticmethod
    def syntax_error_response():
        return JBMPServerResponseMessageMaker.ERROR_response('Syntax Error.')

    @staticmethod
    def no_message_response():
        return JBMPMessage(SERVER_RESPONSE, {'short': 'no_message',
                                             'long': 'No message in queue'}).get_message()
