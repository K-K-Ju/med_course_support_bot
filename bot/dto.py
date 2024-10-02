import datetime


class MessageDTO:
    def __init__(self, _tg_id_, _text_, _datetime_):
        self.tg_id = _tg_id_
        self.text = _text_
        self.datetime = _datetime_


class AdminDTO:
    def __init__(self, _tg_id_, _username_, _name_):
        self.tg_id = _tg_id_
        self.username = _username_
        self.name = _name_
