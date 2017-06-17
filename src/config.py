# -*- coding: utf-8 -*-
import random

conf = dict()

conf["salt"] = "TEST"

conf["server"] = dict()
conf["server"]["ip"] = "0.0.0.0"
conf["server"]["port"] = 9977


def generate_password(len=8):
    pwd = ""
    for i in range(len):
        tmp = random.randint(0, 1)
        if tmp == 0:
            pwd += chr(random.randint(48, 57))
        else:
            pwd += chr(random.randint(65, 90))

    return pwd


class MongoDBCredentials:
    def __init__(self, name=None, ip=None, port=None, user=None, password=None):
        self.name = name
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password


class ServerCredentials:
    def __init__(self, ip=None, port=None):
        self.ip = ip
        self.port = port


class Paths:
    def __init__(self):
        pass
