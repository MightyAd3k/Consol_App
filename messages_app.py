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
parser.add_argument("-s", "--send", help="message")
parser.add_argument("-l", "--list", help="list of messages", action="store_true")
args = parser.parse_args()


def list_all_messages(cur): 
    messages = Message.load_all_messages(cur)
    for message in messages:
        from_ = User.load_user_by_id(cur, message.to_id)
        print("============================================")
        print(f"To: {from_.username}\nSent: {message.creation_date}\nMessage: {message.text}")
        print("============================================")


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

        user = User.load_user_by_username(cursor, args.username)
        validate_password = check_password(args.password, user.hashed_password)
        if user:
            if validate_password:
                if args.username and args.password and args.list:
                    list_all_messages(cursor)
                # elif args.username and args.password and args.delete:
                #     delete_user(cursor, args.username, args.password)
                else:
                    parser.print_help()
            else:
                print("Incorrect password.")
        else:
            print("User does not exist.")
        connection.close()
    except OperationalError:
        print("Connection Error.")
