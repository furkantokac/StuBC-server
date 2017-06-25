# -*- coding: utf-8 -*-
import random, hashlib

# Store sensitive data in credentials.py
# import credentials
import credentials_empty as credentials

token = dict()
token["email"] = "token"  # example


class Conf:
    def __init__(self):
        self.server = credentials.Server()
        self.mondb = credentials.MongoDatabase()

        self.datetime_format = "%y %m %d"


# Send mail to email
def send_mail(email, message):
    return True


def generate_password(len=8):
    pwd = ""
    for i in range(len):
        tmp = random.randint(0, 1)
        if tmp == 0:
            pwd += chr(random.randint(48, 57))
        else:
            pwd += chr(random.randint(97, 112))

    return pwd


def generate_token(unique_str):
    return hasher(generate_password(8) + unique_str + generate_password(8))

# RET : hashed value in string type
def hasher(value):
    return hashlib.sha1(value.encode()).hexdigest()
