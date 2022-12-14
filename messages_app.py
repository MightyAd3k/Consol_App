import psycopg2
from CONSTANTS import HOST, PASSWORD, PORT, USER
from hash_password import check_password
from user_model import User
from messages_model import Message
from psycopg2.errors import OperationalError
import argparse

### TO BE ABLE TO USE THEESE COMMANDS FIRST YOU NEED TO WRITE "python3 users_app.py " ###
##### IN THE CONSOLE, AND THEN COMMANDS. E.G -u {username} or --username {username} #####

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="who should receive the message")
parser.add_argument("-s", "--send", nargs='+', help="message")
parser.add_argument("-l", "--list", help="list of messages", action="store_true")
args = parser.parse_args()


def list_all_messages(cur, user): 
    """
    Lists all messages from database sent by specified user, using command from commands list.

    :param class cursor:
    :param user: author of messages

    Displays all messages sent by the user.
    """

    messages = Message.load_all_messages(cur, user.id)
    for message in messages:
        from_ = User.load_user_by_id(cur, message.from_id)
        to_ = User.load_user_by_id(cur, message.to_id)
        print(f"From: {from_.username}\nTo: {to_.username}\nSent: {message.creation_date}\nMessage: {message.text}")
        print("============================================")


def send_message(cur, from_id, recipient_name, text):
    """
    Create new message using command from command list.
    
    :param class cursor:
    :param int from_id:
    :param str recipient_name:
    :param str text:

    Takes text of the message, checks if it's length is smaller than 255, if isn't print apropriate communicate.
    Checks if recipient of the message exists in databse, if exists, send the message to that user.
    """
    
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
