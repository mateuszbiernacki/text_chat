"""This is the implementation of JSON Based Messaging Protocol [JBMP]."""
import abc

VERSION = '0.1'
ENCODE = 'utf-8'


# Message types list:
SERVER_RESPONSE = 'server_response'


class CryptoInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def encrypt(self, data: bytes):
        pass

    @abc.abstractmethod
    def decrypt(self, data: bytes):
        pass


class JBMPMessage:
    def __init__(self, message_type, data, crypto: CryptoInterface):
        self.version = VERSION
        self.crypto = crypto
        self.message_type = message_type
        self.encode = ENCODE
        self.data = data

    def get_message(self):
        import json
        return json.dumps({'version': self.version,
                           'message_type': self.message_type,
                           'crypto_class': type(self.crypto),
                           'encoding': self.encode,
                           'data': self.crypto.encrypt(self.data)}).encode(self.encode)


class JBMPServerResponseMessageMaker:
    @staticmethod
    def OK_response(long: str):
        return JBMPMessage(SERVER_RESPONSE, {'short': 'OK', 'long': long}).get_message()

    @staticmethod
    def get_list_of_friends_response(list_of_friend: list):
        return JBMPMessage(SERVER_RESPONSE, {'short': 'OK',
                                             'list_of_friends': list_of_friend}).get_message()

    @staticmethod
    def get_public_key_response(public_key):
        return JBMPMessage(SERVER_RESPONSE, {'short': 'pubkey',
                                             'public_key': public_key}).get_message()

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
