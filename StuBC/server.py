# -*- coding: utf-8 -*-

import config, database
from config import Conf
from flask import Flask, jsonify, request
import strings_en as s

db = database.MongoDatabase()
conf = Conf()

app = Flask(__name__)


# Default response with result and message
def default_json_response(result, msg):
    return jsonify(default_dict_response(result, msg))


def default_dict_response(result, msg):
    return dict({"result": result, "msg": msg})


# GET : -
# RET : 'StuBC server is running!'
# DEF : To test if server is running
@app.route('/')
def index():
    return s.MSG_SERVER_RUNNING


# GET : email, username
# RET : true/false, msg
# DEF : User registration, add new user to database, send password to email
@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    email = request.json["email"]
    username = request.json["username"]

    if not db.is_email_allowed(email):
        return default_json_response(False, s.ERR_INVALID_EMAIL_DOMAIN)

    if db.is_email_exist(email):
        return default_json_response(False, s.ERR_DUBLICATED_EMAIL)

    if db.is_username_exist(username):
        return default_json_response(False, s.ERR_DUBLICATED_USERNAME)

    password = config.generate_password()
    db.add_new_user(username, email, password)

    # TODO: Send password to the email
    print(password)

    return default_json_response(True, s.MSG_PASSWORD_SEND_TO_EMAIL)


# GET : email, password
# RET : true/false, msg, username, email, token
# DEF : User login
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    email = request.json["email"]
    password = request.json["password"]

    if not db.is_email_password_match(email, password):
        return default_json_response(False, s.ERR_EMAIL_PASSWORD_NOT_MATCH)

    token = config.generate_token(db.email_to_id(email) + email)
    config.token[email] = token

    resp = default_dict_response(True, s.MSG_LOGIN_SUCCESSFUL)
    resp["token"] = token
    resp["username"] = db.email_to_username(email)
    resp["email"] = email

    return jsonify(resp)


# GET : email
# RET : true/false, msg
# DEF : Recovers the user password by sending new password to the email
@app.route('/user_recovery_password', methods=['GET', 'POST'])
def user_recovery_password():
    email = request.json["email"]

    if not db.is_email_exist(email):
        return default_json_response(False, s.ERR_EMAIL_NOT_EXIST)

    new_password = config.generate_password()

    email_msg = """
    This is a recovery email.
    New password is generated.
    
    Password : {}
    
    Please change your password soon for better security.
    """.format(new_password)
    config.send_mail(email, email_msg)
    db.update_email_password(email, new_password)

    return default_json_response(True, s.MSG_RECOVERY_MAIL_SENT)


# GET : email, password, new_password
# RET : true/false, msg
# DEF : User password update
@app.route('/user_update_password', methods=['GET', 'POST'])
def user_update_password():
    email = request.json["email"]
    password = request.json["password"]
    new_password = request.json["new_password"]

    if not db.is_email_exist(email):
        return default_json_response(False, s.ERR_EMAIL_NOT_EXIST)

    if not db.is_email_password_match(email, password):
        return default_json_response(False, s.ERR_EMAIL_PASSWORD_NOT_MATCH)

    db.update_email_password(email, new_password)

    return default_json_response(True, s.MSG_PASSWORD_UPDATE)


def run():
    app.run(host=conf.server.ip, port=conf.server.port, debug=True)


if __name__ == '__main__':
    run()
