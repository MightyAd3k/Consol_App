import psycopg2
from CONSTANTS import HOST, PASSWORD, PORT, USER
from hash_password import check_password
from user_model import User
from psycopg2.errors import UniqueViolation, OperationalError
import argparse

### TO BE ABLE TO USE THEESE COMMANDS FIRST YOU NEED TO WRITE "python3 users_app.py " ###
##### IN THE CONSOLE, AND THEN COMMANDS. E.G -u {username} or --username {username} #####

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list of all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user' data", action="store_true")
args = parser.parse_args()


def create_user(cur, username, password):
    """
    Create new user using command from commands list.

    :param class cursor:
    :param str username:
    :param str password:

    Takes username and password, first checks if password is min 8 characters long,
    then checks if user of given username exists. In not creates new user, else
    displays apropriate message.
    """

    if len(password) < 8:
        print("Password must be at least 8 characters long.")
    else:
        try:
            user = User(username=username, password=password)
            user.save_user_to_db(cur)
        except UniqueViolation:
            print("User already exists.")


def edit_user(cur, username, password, new_password):
    """
    Edit users password using command from commands list.

    :param class cursor:
    :param str username:
    :param str password:
    :param str new_password:

    Takes username and checks if user exists. If not displays apropriate message, else compares 
    the password from databse with provided password. It they're the same checks length of the new password.
    If it's length is less than 8, print apropriate message, else sets new_password.
    """

    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist.")
    elif check_password(password, new_password):
        if len(new_password) < 8:
            print("New password must be at least 8 characters long.")
        else:
            user.hashed_password = new_password
            user.save_user_to_db(cur)
            print("Password has been changed.")
    else:
        print("Incorrect password.")

    
def delete_user(cur, username, password):
    """
    Delete user from database using command from commands list.

    :param class cursor:
    :param str username:
    :param str password:

    Takes username and checks if user exists. If not displays apropriate message, else compares 
    the password from databse with provided password. It they're the same deletes user from database.
    """

    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist.")
    elif check_password(password, user.hashed_password):
        user.delete_user(cur)
        print("User deleted.")
    else:
        print("Incorrect password.")


def list_all_users(cur):
    """
    Lists all user from database using command from commands list.

    :param class cursor:

    Displays all user names which are in database.
    """

    users = User.load_all_users(cur)
    for user in users:
        print(user.username)


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

        if args.username and args.password and args.edit and args.new_password:
            edit_user(cursor, args.username, args.password, args.new_password)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif  args.list:
            list_all_users(cursor)
        else:
            parser.print_help()
        connection.close()
    except OperationalError:
        print("Connection Error.")
