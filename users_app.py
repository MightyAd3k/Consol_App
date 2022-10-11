from user_model import User
from psycopg2.errors import UniqueViolation
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list of all users")
parser.add_argument("-d", "--delete", help="delete user")
parser.add_argument("-e", "--edit", help="edit user' data")
args = parser.parse_args()


def create_user(cur, username, password):
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cur)
        except UniqueViolation:
            print("User already exists.")

