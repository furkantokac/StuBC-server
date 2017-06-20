# -*- coding: utf-8 -*-


class MsgHandler:
    def __init__(self):
        self.supported_langs = ["ENG"]
        self.selected_lang_code = 0

        self.messages = dict()

        self._add_new_msg(0, "Flask is running!")
        self._add_new_msg(1, "The email domain is not allowed to registration.")
        self._add_new_msg(2, "Email is already registered.")
        self._add_new_msg(3, "Username is already registered.")
        self._add_new_msg(4, "Your password is send to your email.")
        self._add_new_msg(5, "Username and password doesn't match.")
        self._add_new_msg(6, "Login successful.")
        self._add_new_msg(7, "Email doesn't exist.")
        self._add_new_msg(8, "Recovery email is sent to the email.")
        self._add_new_msg(9, "Username doesn't exist.")
        self._add_new_msg(10, "Password is wrong.")
        self._add_new_msg(11, "Your password is updated successfuly.")

    def _add_new_msg(self, msg_code, msg, lang_code=0):
        self.messages[msg_code] = self.supported_langs
        self.messages[msg_code][lang_code] = msg
