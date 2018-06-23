from enum import Enum


class Config(Enum):
    SECRET_KEY = b'oXWerTpO!ThZ!uAAENnV5k9F'
    DATABASE_URI = "postgresql://fr:fr123@localhost/fr"
    HOST = "127.0.0.1"
    PORT = 5000
