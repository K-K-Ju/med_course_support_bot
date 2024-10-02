import sqlite3
from datetime import datetime

from dto import MessageDTO, AdminDTO

db_file_name = 'MessagesDb.db'


class MessageDb:
    def __init__(self):
        self.con = sqlite3.connect(db_file_name)
        self.con.set_trace_callback(print)

    def prepare_db(self):
        self.con.execute('''CREATE TABLE IF NOT EXISTS messages(
                                id INTEGER PRIMARY KEY,
                                tg_id LONG INTEGER,
                                text TEXT NOT NULL, 
                                datetime TEXT);''')

    def add(self, msg_dto: MessageDTO):
        self.con.execute('INSERT INTO messages (tg_id, text, datetime) VALUES (?, ?, ?);',
                         (msg_dto.tg_id, msg_dto.text, msg_dto.datetime))
        self.con.commit()

    def all(self) -> list[MessageDTO]:
        c = self.con.execute('SELECT tg_id, text, datetime FROM messages;')
        rows = c.fetchall()
        msgs = []
        for row in rows:
            msgs.append(MessageDb.from_cursor(row))

        return msgs

    def get_by_user_id(self, tg_id: str) -> list[MessageDTO]:
        c = self.con.execute('SELECT tg_id, text, datetime FROM messages WHERE tg_id=?;', tg_id)
        rows = c.fetchall()
        msgs = []
        for row in rows:
            msgs.append(MessageDb.from_cursor(row))

        return msgs

    def del_by_user_id(self, tg_id: str):
        self.con.execute('DELETE FROM messages WHERE tg_id=?;', tg_id)

    @staticmethod
    def from_cursor(row) -> MessageDTO:
        return MessageDTO(row[0], row[1], datetime.fromisoformat(row[2]))


class AdminDb:
    def __init__(self):
        self.con = sqlite3.connect(db_file_name)
        self.con.set_trace_callback(print)

    def prepare_db(self):
        self.con.execute('''CREATE TABLE IF NOT EXISTS admins(
                                tg_id LONG INTEGER,
                                username TEXT,
                                name TEXT, 
                                active BOOLEAN DEFAULT 1
                                );''')

    def add(self, admin_dto: AdminDTO):
        self.con.execute('INSERT INTO admins (tg_id, username, name) VALUES (?, ?, ?);',
                         (admin_dto.tg_id, admin_dto.username, admin_dto.name))
        self.con.commit()

    def set_active(self, tg_id, is_active: int):
        self.con.execute('UPDATE admins SET active=? WHERE tg_id=?;', (is_active, tg_id))

    def exists(self, tg_id):
        c = self.con.execute(f'SELECT COUNT(tg_id) AS count FROM admins WHERE tg_id={tg_id};')
        res = c.fetchone()[0]
        return res == 1

    def is_active(self, tg_id):
        c = self.con.execute(f'SELECT active FROM admins WHERE tg_id={tg_id};')
        res = c.fetchone()
        if res is None:
            return False

        is_active = res[0]
        return is_active == 1
