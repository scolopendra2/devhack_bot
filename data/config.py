import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

MYSQL_USER = str(os.getenv('MYSQL_USER'))

MYSQL_PASSWORD = str(os.getenv('MYSQL_PASSWORD'))

MYSQL_HOST = str(os.getenv('MYSQL_HOST'))

MYSQL_PORT = str(os.getenv('MYSQL_PORT'))

MYSQL_DBNAME = str(os.getenv('MYSQL_DBNAME'))
