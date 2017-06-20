# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId


class MongoDatabase:
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

    # -------------- BEG USER
    def add_new_user(self, username, email, password):
        coll = self._get_collection(self.coll["user"])

        user = {
            "username": username,
            "password": password,
            "email": email,

            "first_name": "",
            "last_name": "",
            "department": "",
            "rank": 0,
            "interest": "",

            "social": [
            ],

            "permission": [
            ],

            "Token": {
                "token": "",
                "date": ""
            }
        }

        coll.insert(user)

    def is_email_exist(self, email):
        query = {"email": email}
        return self.count_query_result(self.coll["user"], query)

    def is_username_exist(self, username):
        query = {"username": username}
        return self.count_query_result(self.coll["user"], query)

    def is_email_allowed(self, email):
        if not "@" in email:
            return False
        query = {"domain": email.split("@")[1]}
        return self.count_query_result(self.coll["email_domains"], query)

    def password_hash(self, value):
        pass

    # RET : 0 or NUMBER (NUMBER should be 1)
    def is_username_password_match(self, username, password):
        query = {"username": username, "password": password}
        return self.count_query_result(self.coll["user"], query)

    # RET : number of updated field (always should be 1)
    def update_user_password(self, username, new_password):
        return self.update_field(self.coll["user"], {"username": username}, {"password": new_password})

    # RET : username of the corresponding email
    def email_to_username(self, email):
        return self.query_result_single(self.coll["user"], {"email": email})["username"]

    # RET : email of the corresponding username
    def username_to_email(self, username):
        return self.query_result_single(self.coll["user"], {"username": username})["email"]

    # RET : id of the corresponding username
    def username_to_id(self, username):
        return self.query_result_single(self.coll["user"], {"username": username})["_id"]

    # -------------- BEG GENERALS
    # RET : number of updated field
    def update_field(self, collection, find_query, update_query):
        coll = self._get_collection(collection)
        return coll.update(find_query, {"$set": update_query})["n"]

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
