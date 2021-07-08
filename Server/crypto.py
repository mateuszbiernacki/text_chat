import abc
import rsa


class KeysContainer:
    def __init__(self, public, private):
        self.public_key = public
        self.private_key = private


class CryptoInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def encrypt(self, data: bytes, args: list):
        pass

    @abc.abstractmethod
    def decrypt(self, data: bytes, args: list):
        pass

    @staticmethod
    @abc.abstractmethod
    def new_keys(args: list):
        pass


class RSA(CryptoInterface):
    """In encrypt and decrypt function args should look like [public/private key, encrypted_flag].
    If encrypted_flag is equal to False, message would not be encrypted/decrypted."""

    def encrypt(self, data: bytes, args: list):
        if args[1]:
            return rsa.encrypt(data, args[0])
        else:
            return data

    def decrypt(self, data: bytes, args: list):
        if args[1]:
            return rsa.decrypt(data, args[0])
        else:
            return data

    @staticmethod
    def new_keys(args: list):
        return rsa.newkeys(args[0])
