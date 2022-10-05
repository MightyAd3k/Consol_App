HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'postgres'
PORT = 5432

USERS_TABLE = """CREATE TABLE users (
    id serial PRIMARY KEY, 
    username varchar(255) UNIQUE, 
    hashed_password varchar(80)
)"""

MESSAGES_TABLE = """CREATE TABLE messages(
    id SERIAL, 
    from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    to_id INTEGER REFERENCES users(id) ON DELETE CASCADE, 
    text varchar(255),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""
