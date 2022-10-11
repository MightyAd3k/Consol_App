import psycopg2
from CONSTANTS import HOST, PASSWORD, PORT, USER
from hash_password import hash_password

class User:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_user_to_db(self, cursor):
        """
        Add new user to database.
        
        :param class cursor: 

        :rtype: bool
        """
        
        if self._id == -1:
            sql = "INSERT INTO users (username, hashed_password) VALUES(%s, %s) RETURNING id"
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE users SET username=%s, hashed_password=%s WHERE id=%s"
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        """
        Load object from database by given id.

        :param class cursor: 
        :param id_: user's id 

        :rtype: object
        :return: loaded user
        """

        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_username(cursor, username):
        """
        Load object from database by it's username.

        :param class cursor: 
        :param username: user's username

        :rtype: object
        :return: loaded user
        """

        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        """
        Load all objects from database, and them to the list.

        :param class cursor: 

        :rtype: list
        :return: list of all users
        """

        sql = "SELECT id, username, hashed_password FROM users"
        users = []
        cursor.execute(sql, cursor)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete_user(self, cursor):
        """
        Delete object by it's id.

        :param class cursor: 
        
        :rtype: bool
        """

        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True
