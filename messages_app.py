import psycopg2
from messages_model import Message
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="who should receive the message")
parser.add_argument("-s", "--send", help="message")
parser.add_argument("-l", "--list", help="list of messages", action="store_true")
args = parser.parse_args()

