from data_handler import DataHandler
from Protocol.JBMP import JBMPServerResponseMessageMaker as JBMPRes
from crypto import RSA, KeysContainer
import rsa
import socket
import json
import sqlite3
import threading
import queue


class Server:
    def __init__(self):
        self.data_to_send = {}
        for user in DataHandler().db.get_list_of_users():
            self.data_to_send[user] = []
        (self.public_key, self.private_key) = rsa.newkeys(2048)
        print('Key was generated.')
        self.keys = {}
        self.crypto_method = RSA()
        self.messages_queue = queue.Queue()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiving_flag = True
        self.sending_flag = True
        self.sending_thread = threading.Thread(target=self.start_sending)
        self.receiving_thread = threading.Thread(target=self.start_receiving)

    def run(self):
        self.receiving_thread.start()
        self.sending_thread.start()

    def start_receiving(self):
        print('Receiving thread is starting.')
        self.socket.bind(('', 2137))
        while self.receiving_flag:
            try:
                data, address = self.socket.recvfrom(1024)
                threading.Thread(target=self.loop, args=(data, address,)).run()
            except ConnectionResetError:
                continue

    def start_sending(self):
        print('Sending thread is starting.')
        while self.sending_flag:
            if not self.messages_queue.empty():
                (data, address, to_encrypt_flag) = self.messages_queue.get()
                if to_encrypt_flag:
                    self.socket.sendto(rsa.encrypt(data, self.keys[address]), address)
                else:
                    self.socket.sendto(data, address)

    def loop(self, data, address):
        json_data = None
        try:
            data_handler = DataHandler()
            print(data)
            try:
                json_data = json.loads(self.crypto_method.decrypt(data, [self.private_key, True]))
            except:
                json_data = json.loads(self.crypto_method.decrypt(data, [self.private_key, False]))
            json_response = JBMPRes.ERROR_response('Undefined operation.')
            if json_data["command"] == "get_public_key":
                self.keys[address] = rsa.PublicKey(json_data['client_public_key'][0],  # n
                                                   json_data['client_public_key'][1])  # e
                print(self.keys[address])
                json_response = JBMPRes.get_public_key_response([self.public_key.n, self.public_key.e])
            elif json_data["command"] == "login":
                result = data_handler.logg_in(login=json_data["login"], password=json_data["password"], address=address)
                if result == -1:
                    json_response = JBMPRes.not_existing_login_response()
                elif result == -2:
                    json_response = JBMPRes.bad_password_response()
                else:
                    self.data_to_send[json_data["login"]] = []
                    json_response = JBMPRes.success_login_response(result, address)
            elif json_data["command"] == "logout":
                result = data_handler.log_out(login=json_data["login"], token=json_data["token"])
                json_response = data_handler.prepare_standard_response(result)
            elif json_data["command"] == "registration":
                result = data_handler.add_user(login=json_data["login"], password=json_data["password"],
                                               email=json_data["email"])
                if result == 0:
                    json_response = JBMPRes.OK_response("Successfully added new user.")
                elif result == 1:
                    json_response = JBMPRes.occupied_login_response()
            elif json_data["command"] == "invite_friend":
                result = data_handler.save_invite_if_is_possible(login=json_data['login'],
                                                                 friend_login=json_data['friend_login'],
                                                                 token=json_data['token'])

                if result == 0:
                    self.data_to_send[json_data['friend_login']].append({"short": "s_inv_to_friends",
                                                                         "friend_login": json_data["login"]})
                    json_response = JBMPRes.OK_response("Invite was sent.")
                elif result == 4:
                    json_response = JBMPRes.not_existing_friend_login_response()
                elif result == 5:
                    json_response = JBMPRes.ERROR_response("Friend is not logged.")
                else:
                    json_response = data_handler.prepare_standard_response(result)
            elif json_data["command"] == "send_message_to_friend":
                result = data_handler.check_friendship(login=json_data['login'],
                                                       friend_login=json_data['friend_login'],
                                                       token=json_data['token'])

                if result == 0:
                    self.data_to_send[json_data['friend_login']].append({"short": "new_message",
                                                                         "friend_login": json_data["login"],
                                                                         'message': json_data['message']})
                    json_response = JBMPRes.OK_response("Message was sent.")
                elif result == 4:
                    json_response = JBMPRes.not_existing_friend_login_response()
                elif result == 5:
                    json_response = JBMPRes.ERROR_response("Friend is not logged.")
                else:
                    json_response = data_handler.prepare_standard_response(result)
            elif json_data['command'] == 'get_message':
                result = data_handler.is_it_correct_user_token(login=json_data['login'],
                                                               token=json_data['token'])
                if result in {1, 2, 3}:
                    json_response = data_handler.prepare_standard_response(result)
                elif result == 0:
                    if not self.data_to_send[json_data['login']]:
                        json_response = JBMPRes.no_message_response()
                    else:
                        json_response = self.data_to_send[json_data['login']].pop(0)
            elif json_data["command"] == "remove_friend":
                result = data_handler.delete_friend(login=json_data['login'],
                                                    friend_login=json_data['friend_login'],
                                                    token=json_data['token'])
                if result == 0:
                    json_response = JBMPRes.OK_response("User was successfully deleted from friend list.")
                    self.data_to_send[json_data['friend_login']].append({"short": "new_friend",
                                                                         "friend_login": json_data["login"]})
                elif result in {1, 2, 3}:
                    json_response = data_handler.prepare_standard_response(result)
                elif result == 4:
                    json_response = JBMPRes.not_existing_friend_login_response()
                elif result == 5:
                    json_response = JBMPRes.not_your_friend_response()
            elif json_data["command"] == "forgot_password":
                result = data_handler.forgot_password__send_code(login=json_data['login'])
                if result == 0:
                    json_response = JBMPRes.OK_response("Email was sent.")
                elif result == 1:
                    json_response = JBMPRes.not_existing_login_response()
            elif json_data["command"] == "change_password":
                result = data_handler.change_password(login=json_data['login'],
                                                      code=json_data['code'],
                                                      new_password=json_data['new_password'])
                if result == 0:
                    json_response = JBMPRes.OK_response("Password was changed.")
                elif result == 1:
                    json_response = JBMPRes.not_existing_login_response()
                elif result == 2:
                    json_response = JBMPRes.not_generated_code_response()
                elif result == 3:
                    json_response = JBMPRes.bad_code_response()
            elif json_data["command"] == "accept_invite":
                result = data_handler.is_it_correct_user_token(login=json_data['login'], token=json_data['token'])
                if result == 0:
                    result = data_handler.add_friend(login=json_data['login'], friend_login=json_data['friend_login'])
                    if result == 0:
                        self.data_to_send[json_data['friend_login']].append({"short": "new_friend",
                                                                             "friend_login": json_data["login"]})
                        self.data_to_send[json_data['login']].append({"short": "new_friend",
                                                                      "friend_login": json_data["friend_login"]})
                        json_response = JBMPRes.OK_response("Invite was accepted.")
                    elif result == 1:
                        json_response = JBMPRes.not_existing_friend_login_response()
                    elif result == 2:
                        json_response = JBMPRes.ERROR_response("It's your friend already.")
                    elif result == 3:
                        json_response = JBMPRes.ERROR_response("You didn't get invite.")
                else:
                    json_response = data_handler.prepare_standard_response(result)
            elif json_data["command"] == "reject_invite":
                result = data_handler.reject_invite_to_friends_list(login=json_data['login'],
                                                                    token=json_data['token'],
                                                                    friend_login=json_data['friend_login'])
                if result == 0:
                    json_response = JBMPRes.OK_response("Invite was rejected.")
                elif result in {1, 2, 3}:
                    json_response = data_handler.prepare_standard_response(result)
                elif result == 4:
                    json_response = JBMPRes.not_existing_friend_login_response()
                elif result == 5:
                    json_response = JBMPRes.ERROR_response("There is not any invite.")

            elif json_data["command"] == "get_list_of_friends":
                result, list_of_friends = data_handler.get_list_of_friend(login=json_data["login"],
                                                                          token=json_data['token'])
                if result == 0:
                    json_response = JBMPRes.get_list_of_friends_response(list_of_friends)
                else:
                    print(result)
                    json_response = data_handler.prepare_standard_response(result)
        except KeyError:
            json_response = JBMPRes.syntax_error_response()
        except sqlite3.IntegrityError:
            json_response = JBMPRes.ERROR_response("Bad input data.")
        if json_data["command"] == "get_public_key":
            self.messages_queue.put((json_response, address, False))
        else:
            self.messages_queue.put((json_response, address, True))
        print(data_handler.logged_users)


if __name__ == '__main__':
    server = Server()
    server.run()
