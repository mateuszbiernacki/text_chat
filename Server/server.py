import socket
import json
import sqlite3

import rsa
import users

data_to_send = {}
for user in users.db.get_list_of_users():
    data_to_send[user] = []
(public_key, private_key) = rsa.newkeys(2048)
print('Key was generated.')
keys = {}
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 2137))
    data, address = sock.recvfrom(1024)
    JSON_DATA = None
    try:
        print(data)
        try:
            JSON_DATA = json.loads(data.decode('utf-8'))
        except:
            JSON_DATA = json.loads(rsa.decrypt(data, private_key).decode('utf-8'))
        json_response = {
            "short": "Error",
            "long": "Undefined operation."
        }
        if JSON_DATA["command"] == "get_public_key":
            keys[address] = rsa.PublicKey(JSON_DATA['public_key'][0],  # n
                                          JSON_DATA['public_key'][1])  # e
            print(keys[address])
            json_response = {
                "short": "pubkey",
                "pubkey": [public_key.n, public_key.e]
            }
        elif JSON_DATA["command"] == "login":
            result = users.logg_in(login=JSON_DATA["login"], password=JSON_DATA["password"], address=address)
            if result == -1:
                json_response = {
                    "short": "Error",
                    "long": "User is not existed."
                }
            elif result == -2:
                json_response = {
                    "short": "Error",
                    "long": "Bad password."
                }
            else:
                data_to_send[JSON_DATA["login"]] = []

                json_response = {
                    "short": "OK",
                    "long": "Successfully logged.",
                    "token": result,
                    "address": address
                }
        elif JSON_DATA["command"] == "logout":
            result = users.log_out(login=JSON_DATA["login"], token=JSON_DATA["token"])
            json_response = users.prepare_standard_response(result)
        elif JSON_DATA["command"] == "registration":
            result = users.add_user(login=JSON_DATA["login"], password=JSON_DATA["password"], email=JSON_DATA["email"])
            if result == 0:
                json_response = {
                    "short": "OK",
                    "long": "Successfully added new user."
                }
            elif result == 1:
                json_response = {
                    "short": "Error",
                    "long": "Login is occupied."
                }
        elif JSON_DATA["command"] == "invite_friend":
            result = users.save_invite_if_is_possible(login=JSON_DATA['login'],
                                                      friend_login=JSON_DATA['friend_login'],
                                                      token=JSON_DATA['token'])

            if result == 0:
                data_to_send[JSON_DATA['friend_login']].append({"short": "s_inv_to_friends",
                                                                "friend_login": JSON_DATA["login"]})
                json_response = {
                    "short": "OK",
                    "long": "Invite was sent."
                }
            elif result == 4:
                json_response = {
                    "short": "Error",
                    "long": "Friend is not existed."
                }
            elif result == 5:
                json_response = {
                    "short": "Error",
                    "long": "Friend is not logged."
                }
            else:
                json_response = users.prepare_standard_response(result)
        elif JSON_DATA["command"] == "send_message_to_friend":
            result = users.check_friendship(login=JSON_DATA['login'],
                                            friend_login=JSON_DATA['friend_login'],
                                            token=JSON_DATA['token'])

            if result == 0:
                data_to_send[JSON_DATA['friend_login']].append({"short": "new_message",
                                                                "friend_login": JSON_DATA["login"],
                                                                'message': JSON_DATA['message']})
                json_response = {
                    "short": "OK",
                    "long": "Message was sent."
                }
            elif result == 4:
                json_response = {
                    "short": "Error",
                    "long": "Friend is not existed."
                }
            elif result == 5:
                json_response = {
                    "short": "Error",
                    "long": "Friend is not logged."
                }
            else:
                json_response = users.prepare_standard_response(result)
        elif JSON_DATA['command'] == 'get_message':
            result = users.is_it_correct_user_token(login=JSON_DATA['login'],
                                                    token=JSON_DATA['token'])
            if result in {1, 2, 3}:
                json_response = users.prepare_standard_response(result)
            elif result == 0:
                if not data_to_send[JSON_DATA['login']]:
                    json_response = {
                        'short': 'no_message',
                        'long': 'No message in queue'
                    }
                else:
                    json_response = data_to_send[JSON_DATA['login']].pop(0)
        elif JSON_DATA["command"] == "remove_friend":
            result = users.delete_friend(login=JSON_DATA['login'],
                                         friend_login=JSON_DATA['friend_login'],
                                         token=JSON_DATA['token'])
            if result == 0:
                json_response = {
                    "short": "OK",
                    "long": "User was successfully deleted from friend list."
                }
                data_to_send[JSON_DATA['friend_login']].append({"short": "new_friend",
                                                                "friend_login": JSON_DATA["login"]})
            elif result in {1, 2, 3}:
                json_response = users.prepare_standard_response(result)
            elif result == 4:
                json_response = {
                    "short": "Error",
                    "long": "Friend is not existed."
                }
            elif result == 5:
                json_response = {
                    "short": "Error",
                    "long": "This user is not in your friends list."
                }
        elif JSON_DATA["command"] == "forgot_password":
            result = users.forgot_password__send_code(login=JSON_DATA['login'])
            if result == 0:
                json_response = {
                    "short": "OK",
                    "long": "Email was sent."
                }
            elif result == 1:
                json_response = {
                    "short": "Error",
                    "long": "Login is not existed."
                }
        elif JSON_DATA["command"] == "change_password":
            result = users.change_password(login=JSON_DATA['login'],
                                           code=JSON_DATA['code'],
                                           new_password=JSON_DATA['new_password'])
            if result == 0:
                json_response = {
                    "short": "OK",
                    "long": "Password was changed."
                }
            elif result == 1:
                json_response = {
                    "short": "Error",
                    "long": "Login is not existed."
                }
            elif result == 2:
                json_response = {
                    "short": "Error",
                    "long": "Code was not generated."
                }
            elif result == 3:
                json_response = {
                    "short": "Error",
                    "long": "Code is wrong."
                }
        elif JSON_DATA["command"] == "accept_invite":
            result = users.is_it_correct_user_token(login=JSON_DATA['login'], token=JSON_DATA['token'])
            if result == 0:
                result = users.add_friend(login=JSON_DATA['login'], friend_login=JSON_DATA['friend_login'])
                if result == 0:
                    data_to_send[JSON_DATA['friend_login']].append({"short": "new_friend",
                                                                    "friend_login": JSON_DATA["login"]})
                    data_to_send[JSON_DATA['login']].append({"short": "new_friend",
                                                             "friend_login": JSON_DATA["friend_login"]})
                    json_response = {
                        "short": "OK",
                        "long": "Invite was accepted.",
                    }
                elif result == 1:
                    json_response = {
                        "short": "Error",
                        "long": "User with that login doesn't exist.",
                    }
                elif result == 2:
                    json_response = {
                        "short": "Error",
                        "long": "It's your friend already.",
                    }
                elif result == 3:
                    json_response = {
                        "short": "Error",
                        "long": "You didn't get invite.",
                    }
            else:
                json_response = users.prepare_standard_response(result)
        elif JSON_DATA["command"] == "reject_invite":
            result = users.reject_invite_to_friends_list(login=JSON_DATA['login'],
                                                         token=JSON_DATA['token'],
                                                         friend_login=JSON_DATA['friend_login'])
            if result == 0:
                json_response = {
                    "short": "OK",
                    "long": "Invite was rejected.",
                }
            elif result in {1, 2, 3}:
                json_response = users.prepare_standard_response(result)
            elif result == 4:
                json_response = {
                    "short": "Error",
                    "long": "Friend is not existed."
                }
            elif result == 5:
                json_response = {
                    "short": "Error",
                    "long": "There is not any invite."
                }

        elif JSON_DATA["command"] == "get_list_of_friends":
            result, list_of_friends = users.get_list_of_friend(login=JSON_DATA["login"],
                                                               token=JSON_DATA['token'])
            if result == 0:
                json_response = {
                    "short": "OK",
                    "long": "Correct login and token.",
                    "list_of_friends": list_of_friends
                }
            else:
                print(result)
                json_response = users.prepare_standard_response(result)
    except KeyError:
        json_response = {
            "short": "Error",
            "long": "Syntax error."
        }
    except sqlite3.IntegrityError:
        json_response = {
            "short": "Error",
            "long": "Bad input data."
        }
    if json_response["short"] == "pubkey":
        sock.sendto(json.dumps(json_response).encode('utf-8'), address)
    else:
        try:
            sock.sendto(rsa.encrypt(json.dumps(json_response).encode('utf-8'), keys[address]), address)
        except:
            sock.sendto(json.dumps(json_response).encode('utf-8'), address)
    sock.close()
    print(users.logged_users)
