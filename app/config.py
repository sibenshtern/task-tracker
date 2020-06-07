import os
from pathlib import Path

from string import digits, ascii_lowercase
from random import shuffle

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash


load_dotenv()


def generate_random_key():
    """
    Функция, которая генерирует случайный ключ.
    :return: обрезанный hash SHА256
    """
    symbols = list(''.join([digits, ascii_lowercase]))
    shuffle(symbols)

    return generate_password_hash(''.join(symbols)).split("$")[-1]


class Config:
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = 1
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    SECRET_KEY = generate_random_key()
    JSON_AS_ASCII = False

    ADMINS = [MAIL_USERNAME]


class DebugConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False





