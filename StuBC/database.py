# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime
import config


class MongoDatabase:
    # -------------- BEG PRIVATE
    def __init__(self):

        self._connect()
        self.db = self._get_database("stubcTest")

        # Collections
        self.coll = dict()
        self.coll["user"] = "User"
        self.coll["email_domains"] = "EmailDomains"

    def _connect(self):
        try:
            self.client = MongoClient()
            print("MongoDB connection is successful.")
            return True
        except:
            print("MongoDB connection failed!")
            return False

    def _get_database(self, dbname):
        return self.client[dbname]

    def _get_collection(self, collname):
        return self.db[collname]

    def _get_user_collection(self):
        return self.db[self.coll["user"]]

    # -------------- BEG GENERALS
    def insert_element(self, collection, field):
        coll = self._get_collection(collection)
        coll.insert(field)

    # RET : number of updated field
    def update_field(self, collection, find_query, update_query):
        coll = self._get_collection(collection)
        return coll.update(find_query, {"$set": update_query})["n"]

    # RET : number of updated field
    def push_item_to_array(self, collection, find_query, item):
        coll = self._get_collection(collection)
        return coll.update(find_query, {"$push": item})["n"]

    def pull_item_from_array(self, collection, find_query, item):
        coll = self._get_collection(collection)
        return coll.update(find_query, {"$pull": item})["n"]

    # RET : first result of the result of the query
    def query_result_single(self, collection, query):
        coll = self._get_collection(collection)
        return coll.find_one(query)

    # RET : list of the result of the query
    def query_result_multi(self, collection, query):
        coll = self._get_collection(collection)
        return coll.find(query)

    # RET : number of query result
    def count_query_result(self, collection, query):
        coll = self._get_collection(collection)
        return coll.find(query).explain()["n"]

    # RET : hashed value
    def hasher(self, value):
        return config.hasher("thisissalt" + value + "thisissalt")

    def get_datetime(self):
        return datetime.now().strftime(config.Conf().datetime_format)

    def str_to_datetime(self, str_dt):
        return datetime.strptime(str_dt, config.Conf().datetime_format)

    # -------------- BEG USER
    def add_new_user(self, username, email, password):
        user = {
            "username": username,
            "password": self.hasher(password),
            "email": email,

            "first_name": "",
            "last_name": "",
            "department": "",
            "rank": 0,
            "interest": "",

            "register_date": self.get_datetime(),

            "social": [],
            "permission": []
        }

        self.insert_element(self.coll["user"], user)

    def is_email_exist(self, email):
        query = {"email": email}
        return self.count_query_result(self.coll["user"], query)

    def is_username_exist(self, username):
        query = {"username": username}
        return self.count_query_result(self.coll["user"], query)

    def is_email_allowed(self, email):
        if "@" not in email:
            return False
        query = {"domain": email.split("@")[1]}
        return self.count_query_result(self.coll["email_domains"], query)

    def is_username_password_match(self, username, password):
        query = {"username": username, "password": self.hasher(password)}
        return self.count_query_result(self.coll["user"], query)

    def is_email_password_match(self, email, password):
        query = {"email": email, "password": self.hasher(password)}
        return self.count_query_result(self.coll["user"], query)

    # RET : Token
    def append_token(self, username, device_id):
        new_token = config.generate_token(self.username_to_id(username) + device_id)
        token = {
            "token": new_token,
            "device_id": device_id,
            "token_date": self.get_datetime()
        }
        self.push_item_to_array(self.coll["user"], {"username": username}, {"token": token})
        return new_token

    def token_to_username(self, token):
        query = {"token": {"$elemMatch": {"token": token}}}
        return self.query_result_single(self.coll["user"], query)["username"]

    # RET : number of updated field (always should be 1)
    def update_user_password(self, username, new_password):
        return self.update_field(self.coll["user"], {"username": username}, {"password": self.hasher(new_password)})

    # RET : number of updated field (always should be 1)
    def update_email_password(self, email, new_password):
        return self.update_field(self.coll["user"], {"email": email}, {"password": self.hasher(new_password)})

    # RET : username of the corresponding email
    def email_to_username(self, email):
        return self.query_result_single(self.coll["user"], {"email": email})["username"]

    # RET : email of the corresponding username
    def username_to_email(self, username):
        return self.query_result_single(self.coll["user"], {"username": username})["email"]

    # RET : id of the corresponding username
    def username_to_id(self, username):
        return str(self.query_result_single(self.coll["user"], {"username": username})["_id"])

    # RET : id of the corresponding email
    def email_to_id(self, email):
        return str(self.query_result_single(self.coll["user"], {"email": email})["_id"])


if __name__ == "__main__":
    dd = MongoDatabase()
