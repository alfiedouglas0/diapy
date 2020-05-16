from __future__ import annotations
from pysqlcipher3 import dbapi2 as sqlite3  # import sqlite3
from datetime import datetime

# for e.g. 2019-11-19T16:30:05.000
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000"


class DB:
    def __init__(self, path, password: str = None,
                 dateTimeFormat=DATE_TIME_FORMAT):
        self._dateTimeFormat = dateTimeFormat
        self._conn = sqlite3.connect(path)
        self._cursor = self._conn.cursor()
        if password != None:
            self._cursor.execute('pragma key="{}"'.format(password))

    def __enter__(self) -> db:
        return self

    def save(self):
        self._conn.commit()

    def get_previous_inserted_row_id(self) -> int:
        self._cursor.execute("""SELECT last_insert_rowid();""")
        unparsedResult = self._cursor.fetchone()
        return unparsedResult[0]

    def get_entry(self, id: int) -> DB_Entry:
        self._cursor.execute("""SELECT * FROM entries
                                WHERE id=? LIMIT 1""", (id,))
        return DB_Entry(*self._cursor.fetchone())

    def remove_entry(self, id: int):
        self._cursor.execute("""DELETE FROM entries
                                WHERE id=?;""", (id,))

    def new_entry_body_pair(self):
        return DB_Entry(-1, datetime.now(), datetime.now(), datetime.now(),
                        '', -1, 1), DB_Entry_Body(-1, '')

    def insert_or_update_entry(self, entry: DB_Entry) -> DB_Entry:
        if(entry.id < 0):  # means it does not in the db
            self._cursor.execute("""
                INSERT INTO entries (entry_date, date_created, last_modified,
                title, entry_body_id) VALUES (?, ?, ?, ?, ?); """,
                                 (entry.entry_date.strftime(self._dateTimeFormat),
                                  entry.date_created.strftime(
                                     self._dateTimeFormat),
                                  entry.last_modified.strftime(
                                     self._dateTimeFormat),
                                  entry.title, entry.entry_body_id))
            entry.id = self.get_previous_inserted_row_id()
        else:
            self._cursor.execute("""
                UPDATE entries SET entry_date=?, date_created=?, last_modified=?,
                     title=?, entry_body_id=?
                WHERE id=?;""",
                                 (entry.entry_date.strftime(self._dateTimeFormat),
                                  entry.date_created.strftime(
                                     self._dateTimeFormat),
                                  entry.last_modified.strftime(
                                     self._dateTimeFormat),
                                     entry.title, entry.entry_body_id, entry.id))
        return entry

    def get_all_entries(self, visible=True, ordered=True) -> [DB_Entry]:
        self._cursor.execute("""SELECT id FROM entries {} {};""".format(
            """WHERE visible != 0""" if visible else "",
            """ORDER BY entry_date DESC""" if ordered else ""
        ))
        unparsedEntries = self._cursor.fetchall()
        return [self.get_entry(unparsedItem[0])
                for unparsedItem in unparsedEntries]

    def get_entry_body(self, id: int) -> DB_Entry:
        self._cursor.execute("""SELECT * FROM entry_bodies
                                WHERE id=? LIMIT 1""", (id,))
        return DB_Entry_Body(*self._cursor.fetchone())

    def insert_or_update_entry_body(self, body: DB_Entry_Body) -> DB_Entry_Body:
        if(body.id < 0):  # means it does not in the db
            self._cursor.execute("""
                INSERT INTO entry_bodies (body) VALUES (?);""",
                                 (body.body,))
            body.id = self.get_previous_inserted_row_id()
        else:
            self._cursor.execute("""
                UPDATE entry_bodies SET body=? WHERE id=?;""",
                                 (body.body, body.id))
        return body

    def get_tag(self, id: int) -> DB_Tag:
        self._cursor.execute("""SELECT * FROM tags
                                    WHERE id=? LIMIT 1""", (id,))
        return DB_Tag(*self._cursor.fetchone())

    def remove_tag(self, id: int):
        self._cursor.execute("""DELETE FROM tags
                                WHERE id=?;""", (id,))


class DB_Entry:
    def __init__(self, id: int, entry_date: str, date_created: str,
                 last_modified: str, title: str, entry_body_id: int,
                 visible: int):
        self._id = id
        self._entry_date = datetime.strptime(
            entry_date, DATE_TIME_FORMAT) if isinstance(entry_date, str) else entry_date
        self._date_created = datetime.strptime(
            date_created, DATE_TIME_FORMAT) if isinstance(date_created, str) else date_created
        self._last_modified = datetime.strptime(
            last_modified, DATE_TIME_FORMAT) if isinstance(last_modified, str) else last_modified
        self._title = title
        self._entry_body_id = entry_body_id
        self._visible = visible

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, val):
        assert isinstance(val, int)
        self._id = val

    @property
    def entry_date(self) -> datetime:
        return self._entry_date

    @entry_date.setter
    def entry_date(self, val):
        assert isinstance(val, str) or isinstance(val, datetime)
        self._entry_date = datetime.strptime(
            val, DATE_TIME_FORMAT) if isinstance(val, str) else val

    @property
    def date_created(self) -> datetime:
        return self._date_created

    @date_created.setter
    def date_created(self, val):
        assert isinstance(val, str) or isinstance(val, datetime)
        self._date_created = datetime.strptime(
            val, DATE_TIME_FORMAT) if isinstance(val, str) else val

    @property
    def last_modified(self) -> datetime:
        return self._last_modified

    @last_modified.setter
    def last_modified(self, val):
        assert isinstance(val, str) or isinstance(val, datetime)
        self._last_modified = datetime.strptime(
            val, DATE_TIME_FORMAT) if isinstance(val, str) else val

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, val):
        assert isinstance(val, str)
        self._title = val

    @property
    def entry_body_id(self) -> int:
        return self._entry_body_id

    @entry_body_id.setter
    def entry_body_id(self, val):
        assert isinstance(val, int)
        self._entry_body_id = val

    @property
    def visible(self) -> int:
        return self._visible

    @visible.setter
    def visible(self, val):
        assert isinstance(val, int)
        self._visible = val


class DB_Tag:
    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, val):
        assert isinstance(val, int)
        self._id = val

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, val):
        assert isinstance(val, str)
        self._name = val


class DB_Entry_Body:
    def __init__(self, id: int, body: str):
        self._id = id
        self._body = body

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, val):
        assert isinstance(val, int)
        self._id = val

    @property
    def body(self) -> str:
        return self._body

    @body.setter
    def body(self, val):
        assert isinstance(val, str)
        self._body = val


class DB_Entry_tag:
    def __init__(self, entry_id: int, tag_id: int):
        self._entry_id = entry_id
        self._tag_id = tag_id

    @property
    def entry_id(self) -> int:
        return self._entry_id

    @entry_id.setter
    def entry_id(self, val):
        assert isinstance(val, int)
        self._entry_id = val

    @property
    def tag_id(self) -> str:
        return self._tag_id

    @tag_id.setter
    def tag_id(self, val):
        assert isinstance(val, int)
        self._tag_id = val
