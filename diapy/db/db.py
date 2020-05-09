from __future__ import annotations
from pysqlcipher3 import dbapi2 as sqlite3  # import sqlite3
from datetime import datetime

# for e.g. 2019-11-19T16:30:05.000-0000
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000%z"


class DB:
    def __init__(self, path, password: str = None):
        self._dateTimeFormat = DATE_TIME_FORMAT
        self._conn = sqlite3.connect(path)
        self._cursor = self._conn.cursor()
        if password != None:
            self._cursor.execute('pragma key="{}"'.format(password))

    def __enter__(self) -> db:
        return self

    def get_entry(self, id: int) -> DB_Entry:
        self._cursor.execute("""SELECT * FROM entries
                                WHERE id=? LIMIT 1""", (id,))
        return DB_Entry(*self._cursor.fetchone())

    def remove_entry(self, id: int):
        self._cursor.execute("""DELETE FROM entries
                                WHERE id=?;""", (id,))

    def get_all_entries(self) -> [DB_Entry]:
        self._cursor.execute("""SELECT id FROM entries""")
        unparsedEntries = self._cursor.fetchall()
        return [self.get_entry(unparsedItem[0])
                for unparsedItem in unparsedEntries]

    def get_entry_body(self, id: int) -> DB_Entry:
        self._cursor.execute("""SELECT * FROM entry_bodies
                                WHERE id=? LIMIT 1""", (id,))
        return DB_Entry_Body(*self._cursor.fetchone())

    def get_tag(self, id: int) -> DB_Tag:
        self._cursor.execute("""SELECT * FROM tags
                                    WHERE id=? LIMIT 1""", (id,))
        return DB_Tag(*self._cursor.fetchone())

    def remove_tag(self, id: int):
        self._cursor.execute("""DELETE FROM tags
                                WHERE id=?;""", (id,))


class DB_Entry:
    def __init__(self, id: int, entry_date: str, date_created: str,
                 last_modified: str, title: str, entry_body_id: int):
        self._id = id
        self._entry_date = datetime.strptime(entry_date, DATE_TIME_FORMAT)
        self._date_created = datetime.strptime(date_created, DATE_TIME_FORMAT)
        self._last_modified = datetime.strptime(
            last_modified, DATE_TIME_FORMAT)
        self._title = title
        self._entry_body_id = entry_body_id

    @property
    def id(self) -> int:
        return self._id

    @property
    def entry_date(self) -> datetime:
        return self._entry_date

    @property
    def date_created(self) -> datetime:
        return self._date_created

    @property
    def last_modified(self) -> datetime:
        return self._last_modified

    @property
    def title(self) -> str:
        return self._title

    @property
    def entry_body_id(self) -> int:
        return self._entry_body_id


class DB_Tag:
    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class DB_Entry_Body:
    def __init__(self, id: int, body: str):
        self._id = id
        self._body = body

    @property
    def id(self) -> int:
        return self._id

    @property
    def body(self) -> str:
        return self._body


class DB_Entry_tag:
    def __init__(self, entry_id: int, tag_id: int):
        self._entry_id = entry_id
        self._tag_id = tag_id

    @property
    def entry_id(self) -> int:
        return self._entry_id

    @property
    def tag_id(self) -> str:
        return self._tag_id
