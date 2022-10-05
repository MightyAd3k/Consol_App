# psql command: psql -h localhost -U postgres -W
# password = postgres

import psycopg2
from psycopg2.errors import DuplicateDatabase, DuplicateTable, OperationalError

from CONSTANTS import HOST, USER, PASSWORD, PORT, USERS_TABLE, MESSAGES_TABLE

def connect_to_server():
    """Connect with the server and create new database. If database already exists, show proper communicate."""

    global db_name
    try:
        connection = psycopg2.connect(
            host=HOST, 
            user=USER, 
            password=PASSWORD,
            port = PORT
        )
        print('Server connected.\n')

        connection.autocommit = True
        cursor = connection.cursor()

        db_name = input('Enter new databse name: ')

        check_db_list = 'SELECT datname FROM pg_database;'
        cursor.execute(check_db_list)
        list_of_databases = cursor.fetchall()

        try:
            (db_name,) in list_of_databases
        except DuplicateDatabase:
            print(f'Database "{db_name}" already exists.')
        else:
            create_db = f'CREATE DATABASE {db_name};'
            cursor.execute(create_db)
            print(f'Database "{db_name}" created succesfully.\n')
            
        connection.close()
    except OperationalError:
        print('Server not connected.')

def create_tables():
    """Create tables in database. If tables already exist, inform user about it."""

    try:
        connection = psycopg2.connect(
            host=HOST, 
            user=USER, 
            password=PASSWORD,
            port = PORT,
            database = db_name
        )
        print('Server connected.\n')

        connection.autocommit = True
        cursor = connection.cursor()

        try:
            cursor.execute(USERS_TABLE)
            print('Table "users" created.')
        except DuplicateTable:
            print('Table "users" already exists.')
        
        try:
            cursor.execute(MESSAGES_TABLE)
            print('Table "messages" created.')
        except DuplicateTable:
            print('Table "users" already exists.')

        connection.close()
    except OperationalError:
        print('Server not connected.')


connect_to_server()
create_tables()
