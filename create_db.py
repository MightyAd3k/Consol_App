# psql command: psql -h localhost -U postgres -W
# password = postgres

import psycopg2
from psycopg2.errors import DuplicateDatabase, DuplicateTable


HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'postgres'
PORT = 5432

### CONNECT TO DB ###
try:
    connection = psycopg2.connect(
        host=HOST, 
        user=USER, 
        password=PASSWORD,
        port = PORT
    )
    print('Database connected')
except:
    print('Database not connected')

if connection is not None:
    connection.autocommit = True

    cursor = connection.cursor()

    db_name = input('Enter new databse name: ')

    sql = 'SELECT datname FROM pg_database;'
    cursor.execute(sql)
    list_of_databases = cursor.fetchall()
   
    ### CHECK IF DATABASE ALREADY EXISTS ###
    if (db_name,) in list_of_databases:
        raise DuplicateDatabase(f'Database "{db_name}" already exists')
    else:
        sql1 = f'CREATE DATABASE {db_name};'
        cursor.execute(sql1)
        print(f'Database "{db_name}" created succesfully')

    connection.close()
    print('Done')
