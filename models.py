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

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO users (username, hashed_password) VALUES(%s, %s) RETURNING id"
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        return False
    



# connection = psycopg2.connect(
#             host=HOST, 
#             user=USER, 
#             password=PASSWORD,
#             port = PORT,
#             database = "console_app_db"
#         )


# connection.autocommit = True
# cursor = connection.cursor()
# new_user = User('Adek', 'password123')
# new_user.save_to_db(cursor)