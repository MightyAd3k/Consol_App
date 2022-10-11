from psycopg2 import connect
from CONSTANTS import HOST, PASSWORD, PORT, USER

class Message:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None

    @property
    def id(self):
        return self._id

    def save_message_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO messages (from_id, to_id, text, creation_date) VALUES(%s, %s, %s, %s RETURNING id"
            values = (self.from_id, self.to_id, self.text, self.creation_date)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = "UPDATE messages SET to_id=%s, text=%s WHERE id=%s"
            values = (self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True


    def load_all_messages(self, cursor):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
        messages = []
        cursor.execute(sql, cursor)
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Message()
            loaded_message.id = id_
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.text = text
            loaded_message.creation_date = creation_date
            messages.append(loaded_message)
        return messages


# sql = "INSERT INTO messages (from_id, to_id, text) VALUES (%s, %s, %s)"
# values = (1, 8, 'Cześć Angelika!')
# connection = connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database="console_app_db")
# connection.autocommit = True
# cursor = connection.cursor()
# cursor.execute(sql, values)
# connection.commit()
