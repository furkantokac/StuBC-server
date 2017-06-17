# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
import database, config
from config import conf

db = database.MongoDatabase()

app = Flask(__name__)


# Default response with result and message
def default_json_response(result, msg):
    return jsonify({"result": result, "msg": msg})


# Send mail to email
def send_mail(email, message):
    return True


# GET : -
# RET : 'Flask is running!'
# DEF : To test if server is running
@app.route('/')
def index():
    return 'Flask is running!'


# GET : email, username
# RET : true/false, msg
# DEF : User registration, add new user to database
@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    email = request.json["email"]
    username = request.json["username"]

    if not db.is_email_allowed(email):
        return default_json_response(False, "The email domain is not allowed to registration.")

    if db.is_email_exist(email):
        return default_json_response(False, "Email is already registered.")

    if db.is_username_exist(username):
        return default_json_response(False, "Username is already registered.")

    password = config.generate_password()
    db.add_new_user(username, email, password)

    # TODO: Send password to the email
    print(password)

    return default_json_response(True, "Your password is send to your email.")


# GET : username, password
# RET : true/false, msg
# DEF : User login
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    username = request.json["username"]
    password = request.json["password"]

    if not db.is_username_password_match(username, password):
        return default_json_response(False, "Username and password doesn't match.")

    return default_json_response(True, "Login successful.")


# GET : email
# RET : true/false, msg
# DEF : User login
@app.route('/user_recovery_password', methods=['GET', 'POST'])
def user_recovery_password():
    email = request.json["email"]

    if not db.is_email_exist(email):
        return default_json_response(False, "Email doesn't exist.")

    username = db.email_to_username(email)
    new_password = config.generate_password()

    email_msg = """
    This is a recovery email.
    New password is generated.
    
    Username = {}
    Password : {}
    """.format(username, new_password)
    send_mail(email, email_msg)
    db.update_user_password(username, new_password)

    return default_json_response(True, "Recovery email is sent to '{}'".format(email))


# GET : username, password, new_password
# RET : true/false, msg
# DEF : User password update
@app.route('/user_update_password', methods=['GET', 'POST'])
def user_update_password():
    username = request.json["username"]
    password = request.json["password"]
    new_password = request.json["new_password"]

    if not db.is_username_exist(username):
        return default_json_response(False, "Username doesn't exist.")

    if not db.is_username_password_match(username, password):
        return default_json_response(False, "Password is wrong.")

    db.update_user_password(username, new_password)

    return default_json_response(True, "Password is updated for '{}'".format(username))


def run():
    app.run(host=conf["server"]["ip"], port=conf["server"]["port"], debug=True)


if __name__ == '__main__':
    run()
