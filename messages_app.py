import psycopg2
from hash_password import check_password
from user_model import User
from messages_model import Message
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="who should receive the message")
parser.add_argument("-s", "--send", help="message")
parser.add_argument("-l", "--list", help="list of messages", action="store_true")
args = parser.parse_args()


def list_all_messages(cur, username, password):
    user = User.load_user_by_username(username)
    validate_password = check_password(password)
    if user:
        if validate_password:    
            messages = Message.load_all_messages(cur)
            for message in messages:
                print("================================================================")
                print(f"Message receiver: {message.to_id}\nMessage sent: {message.creation_date}\nMessage: {message.text}")
                print("================================================================")
        else:
            print("Incorrect password.")
    else:
        print("User does not exist.")

