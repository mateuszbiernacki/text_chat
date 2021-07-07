from random import randrange
from _smtp import send_email
from database_connector import DBConnector

PATH_TO_USERS_DATABASE = 'TestData/users.db'


class DataHandler:
    db = DBConnector()
    logged_users = {}

    @staticmethod
    def add_user(*, login, password, email):
        """Returns 0 when process of adding new users was correct.
        Returns 1 when login is occupied."""
        if DataHandler.db.check_user_exits(login):
            return 1
        else:
            DataHandler.db.add_user(login, password, email)
            return 0

    @staticmethod
    def logg_in(*, login, password, address):
        """Returns -2 when password is wrong.
        Returns -1 when user is not exist.
        Returns token when user was successfully logged."""
        if DataHandler.db.check_user_exits(login):
            if DataHandler.db.check_user_password(login, password):
                token = DataHandler.generate_token()
                DataHandler.logged_users[login] = (token, address)
                return token
            else:
                return -2
        else:
            return -1

    @staticmethod
    def log_out(*, login, token):
        """Returns 0 when user was successfully logged out.
        Returns 1 when token is incorrect.
        Returns 2 when user with that login is not logged.
        Returns 3 when user with that login is not exist."""
        result = DataHandler.is_it_correct_user_token(login=login, token=token)
        if result == 0:
            print('Logged out: ', login, DataHandler.logged_users.pop(login))
            return 0
        return result

    @staticmethod
    def save_invite_if_is_possible(*, login, friend_login, token):
        """Returns 0 when invite was saved.
            Returns 1 when token is incorrect.
            Returns 2 when user with that login is not logged.
            Returns 3 when user with that login is not exist.
            Returns 4 when friend is not existed.
            Returns 5 when friend is not logged."""

        result = DataHandler.is_it_correct_user_token(login=login, token=token)
        if result == 0:
            if DataHandler.db.check_user_exits(friend_login):
                if friend_login in DataHandler.logged_users:
                    if DataHandler.db.check_invite(login, friend_login):
                        return 0
                    else:
                        DataHandler.db.add_invite(login, friend_login)
                    return 0
                else:
                    return 5
            else:
                return 4
        else:
            return result

    @staticmethod
    def check_friendship(*, login, friend_login, token):
        """Returns 0 when it's a friend.
            Returns 1 when token is incorrect.
            Returns 2 when user with that login is not logged.
            Returns 3 when user with that login is not exist.
            Returns 4 when friend is not existed.
            Returns 5 when friend is not logged."""

        result = DataHandler.is_it_correct_user_token(login=login, token=token)
        if result == 0:
            if DataHandler.db.check_user_exits(friend_login):
                if friend_login in DataHandler.logged_users:

                    return 0
                else:
                    return 5
            else:
                return 4
        else:
            return result

    @staticmethod
    def get_address_by_login(*, login):
        return DataHandler.logged_users[login][1]

    @staticmethod
    def is_invited(*, login, friend_login):
        """Returns 0 when user was invited by friend.
            Returns 1 when he was not."""
        if DataHandler.db.check_invite(login, friend_login):
            return 0
        return 1

    @staticmethod
    def add_friend(*, login, friend_login):
        """Returns 0 when process of adding new friend was correct.
        Returns 1 when friend is not exits.
        Returns 2 when friend is on your friends list already.
        Returns 3 when friend is not invited you."""
        if DataHandler.db.check_user_exits(login):
            if DataHandler.db.check_user_exits(friend_login):
                if DataHandler.db.check_friendship(login, friend_login):
                    return 2
                elif DataHandler.db.check_invite(friend_login, login):
                    DataHandler.db.set_new_friend(login, friend_login)
                    DataHandler.db.delete_invite(friend_login, login)
                    return 0
                return 3
            else:
                return 1
        else:
            return 1

    @staticmethod
    def reject_invite_to_friends_list(*, login, friend_login, token):
        """Returns 0 when invite was rejected.
            Returns 1 when token is incorrect.
            Returns 2 when user with that login is not logged.
            Returns 3 when user with that login is not exist.
            Returns 4 when friend login is not existed.
            Returns 5 when there is not any invite."""
        result = DataHandler.is_it_correct_user_token(login=login, token=token)
        if result == 0:
            if DataHandler.db.check_user_exits(friend_login):
                if DataHandler.db.check_invite(friend_login, login):
                    DataHandler.db.delete_invite(friend_login, login)
                    return 0
                else:
                    return 5
            else:
                return 4
        else:
            return result

    @staticmethod
    def delete_friend(*, login, friend_login, token):
        """Returns 0 when process of deleting new friend was correct.
            Returns 1 when token is incorrect.
            Returns 2 when user with that login is not logged.
            Returns 3 when user with that login is not exist.
            Returns 4 when friend login is not existed.
            Returns 5 when that is not your current friend."""
        result = DataHandler.is_it_correct_user_token(login=login, token=token)
        if result == 0:
            if DataHandler.db.check_user_exits(friend_login):
                if DataHandler.db.check_friendship(login, friend_login):
                    DataHandler.db.delete_friendship(login, friend_login)
                    return 0
                else:
                    return 5
            else:
                return 4
        else:
            return result

    @staticmethod
    def get_list_of_friend(*, login, token):
        """Returns 0 and friends list when everything is correct.
            Returns 1 when token is incorrect.
            Returns 2 when user with that login is not logged.
            Returns 3 when user with that login is not exist."""
        result = DataHandler.is_it_correct_user_token(login=login, token=token)
        if result == 0:
            return 0, DataHandler.db.get_list_of_friend(login)
        else:
            return result, []

    @staticmethod
    def forgot_password__send_code(*, login):
        """Return 0 when code was send.
        Return 1 when it was not."""
        if DataHandler.db.check_user_exits(login):
            code = DataHandler.generate_token()
            if DataHandler.db.check_login_in_codes(login):
                DataHandler.db.delete_code(login)
            send_email(to=DataHandler.db.get_user_email(login),
                       subject='Authentication Code',
                       message=f'Your code: {code}')
            DataHandler.db.add_code(login, str(code))
            return 0
        else:
            return 1

    @staticmethod
    def change_password(*, login, code, new_password):
        """Return 0 when password was successfully changed.
        Return 1 when that login is not existed.
        Return 2 when there is not generated code yet.
        Return 3 when code is wrong."""
        if DataHandler.db.check_user_exits(login):
            if DataHandler.db.check_login_in_codes(login):
                if DataHandler.db.check_code(login, str(code)):
                    DataHandler.db.change_password(login, new_password)
                    DataHandler.db.delete_code(login)
                    return 0
                else:
                    return 3
            else:
                return 2
        else:
            return 1

    @staticmethod
    def generate_token():
        return randrange(0, 2 ** 64)

    @staticmethod
    def is_it_correct_user_token(*, login, token):
        """Returns 0 when token is correct.
        Returns 1 when token is incorrect.
        Returns 2 when user with that login is not logged.
        Returns 3 when user with that login is not exist."""
        if DataHandler.db.check_user_exits(login):
            if login in DataHandler.logged_users:
                if token == DataHandler.logged_users[login][0]:
                    return 0
                else:
                    return 1
            else:
                return 2
        else:
            return 3

    @staticmethod
    def prepare_standard_response(int_result):
        if int_result == 0:
            json_response = {
                "short": "OK",
                "long": "Successfully logged out.",
            }
        elif int_result == 1:
            json_response = {
                "short": "Error",
                "long": "Wrong token."
            }
        elif int_result == 2:
            json_response = {
                "short": "Error",
                "long": "Users is not logged."
            }
        elif int_result == 3:
            json_response = {
                "short": "Error",
                "long": "Users is not existed."
            }
        else:
            json_response = {
                "short": "BigError",
                "long": "Wrong argument in prepare_standard_response(int_result). Please contact with administrator."
            }
        return json_response
