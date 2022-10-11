from hash_password import check_password
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


def edit_password(cur, username, password, new_password):
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist.")
    elif check_password(password, new_password):
        if len(new_password) < 8:
            print("New password must be at least 8 characters long.")
        else:
            user.hashed_password = new_password
            user.save_to_db(cur)
            print("Password has been changed.")
    else:
        print("Incorrect password.")

    
def delete_user(cur, username, password):
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist.")
    elif check_password(password, user.hashed_password):
        user.delete_user(cur)
        print("User deleted.")
    print("Incorrect password.")


