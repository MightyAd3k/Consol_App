import psycopg2
from CONSTANTS import HOST, PASSWORD, PORT, USER
from hash_password import check_password
from user_model import User
from messages_model import Message
from psycopg2.errors import OperationalError
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="who should receive the message")
parser.add_argument("-s", "--send", nargs='+', help="message")
parser.add_argument("-l", "--list", help="list of messages", action="store_true")
args = parser.parse_args()


def list_all_messages(cur, user): 
    messages = Message.load_all_messages(cur, user.id)
    for message in messages:
        from_ = User.load_user_by_id(cur, message.from_id)
        to_ = User.load_user_by_id(cur, message.to_id)
        print(f"From: {from_.username}\nTo: {to_.username}\nSent: {message.creation_date}\nMessage: {message.text}")
        print("============================================")


def send_message(cur, from_id, recipient_name, text):
    if len(text) <= 255:
        to_ = User.load_user_by_username(cur, recipient_name)
        if to_:
            message = Message(from_id, to_.id, text=text)
            message.save_message_to_db(cur)
            print("Message send.")
    else:
        print("Message is too long.")


if __name__ == "__main__":
    try:
        connection = psycopg2.connect(
                host=HOST, 
                user=USER, 
                password=PASSWORD,
                port = PORT,
                database = "console_app_db"
            )
        connection.autocommit = True
        cursor = connection.cursor()

        if args.username and args.password:
            user = User.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.list:
                    list_all_messages(cursor, user)
                elif args.to and args.send:
                    send_message(cursor, user.id, args.to, ' '.join(args.send))
                else:
                    parser.print_help()
            else:
                print("Incorrect password.")
        else:
            print("User does not exist.")
        connection.close()
    except OperationalError:
        print("Connection Error.")
