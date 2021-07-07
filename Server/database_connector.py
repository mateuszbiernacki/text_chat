import sqlite3

PATH_TO_USERS_DATABASE = 'Data/data.db'


def install_database():
    database_connection = sqlite3.connect(PATH_TO_USERS_DATABASE)
    cursor = database_connection.cursor()
    cursor.execute('create table users (login text primary key, password text, email text unique)')
    cursor.execute('create table friends (login text not null, friend_login text not null, '
                   'foreign key (login, friend_login) references users (login, login),'
                   'unique (login, friend_login))')
    cursor.execute('create table invites (_from text not null, _to text not null,'
                   'foreign key (_from, _to) references users (login, login),'
                   'unique (_from, _to))')
    cursor.execute('create table codes (login text not null, code text not null,'
                   'foreign key (login) references users (login),'
                   'unique (login))')
    database_connection.commit()
    database_connection.close()


class DBConnector:

    def __init__(self, path=PATH_TO_USERS_DATABASE):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def add_user(self, login, password, email):
        self.cursor.execute('insert into users values (?, ?, ?)', (login, password, email))
        self.connection.commit()

    def check_user_exits(self, login: str) -> bool:
        self.cursor.execute('select * from users where login=:login', {'login': login})
        if not self.cursor.fetchall():
            return False
        else:
            return True

    def check_user_password(self, login, password) -> bool:
        self.cursor.execute('select password from users where login=:login', {'login': login})
        row = self.cursor.fetchone()
        if not row:
            return False
        elif row[0] == password:
            return True
        else:
            return False

    def get_user_email(self, login) -> str:
        self.cursor.execute('select email from users where login=:login', {'login': login})
        row = self.cursor.fetchone()
        if not row:
            return ''
        else:
            return row[0]

    def get_list_of_users(self) -> []:
        self.cursor.execute('select login from users')
        return [user_tuple[0] for user_tuple in self.cursor.fetchall()]

    def add_invite(self, login, friend_login):
        self.cursor.execute('insert into invites values (?, ?)', (login, friend_login))
        self.connection.commit()

    def delete_invite(self, login, friend_login):
        self.cursor.execute('delete from invites where _from=:login and _to=:friend_login',
                            {'login': login, 'friend_login': friend_login})
        self.connection.commit()

    def check_invite(self, login, friend_login) -> bool:
        self.cursor.execute('select * from invites where _from=:login and _to=:friend_login',
                            {'login': login, 'friend_login': friend_login})
        if not self.cursor.fetchall():
            return False
        else:
            return True

    def add_code(self, login, code):
        self.cursor.execute('insert into codes values (?, ?)', (login, code))
        self.connection.commit()

    def delete_code(self, login):
        self.cursor.execute('delete from codes where login=:login',
                            {'login': login})
        self.connection.commit()

    def check_login_in_codes(self, login) -> bool:
        self.cursor.execute('select * from codes where login=:login',
                            {'login': login})
        if not self.cursor.fetchall():
            return False
        else:
            return True

    def check_code(self, login, code) -> bool:
        self.cursor.execute('select * from codes where login=:login and code=:code',
                            {'login': login, 'code': code})
        if not self.cursor.fetchall():
            return False
        else:
            return True

    def set_new_friend(self, login, friend_login):
        self.cursor.execute('insert into friends values (?, ?)', (login, friend_login))
        self.cursor.execute('insert into friends values (?, ?)', (friend_login, login))
        self.connection.commit()

    def delete_friendship(self, login, friend_login):
        self.cursor.execute('delete from friends where login=:login and friend_login=:friend_login',
                            {'login': login, 'friend_login': friend_login})
        self.cursor.execute('delete from friends where login=:login and friend_login=:friend_login',
                            {'login': friend_login, 'friend_login': login})
        self.connection.commit()

    def get_list_of_friend(self, login) -> []:
        self.cursor.execute('select friend_login from friends where login=:login', {'login': login})
        return [friend_tuple[0] for friend_tuple in self.cursor.fetchall()]

    def check_friendship(self, login, friend_login) -> bool:
        self.cursor.execute('select * from friends where login=:login and friend_login=:friend_login',
                            {'login': login, 'friend_login': friend_login})
        if not self.cursor.fetchall():
            return False
        else:
            return True

    def change_password(self, login, new_password):
        self.cursor.execute('update users set password=:pass where login=:log',
                            {'log': login, 'pass': new_password})
        self.connection.commit()


if __name__ == '__main__':
    db = DBConnector()
    # db.add_user('mati', '123', 'mail@123')
    # db.add_user('mati1', '123', 'mail@1232')
    # print(db.get_list_of_users())
    # db.set_new_friend('bat', 'pat')
    # db.delete_friendship('mati1', 'mati')
    # print(db.get_list_of_users())
    # print(db.check_friendship('mati', 'mati1'))
    # install_database()
