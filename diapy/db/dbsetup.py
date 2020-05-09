from pysqlcipher3 import dbapi2 as sqlite3  # import sqlite3


def create_db(path: str, password: str = None):
    """ Creates db like so:
            entries:
                0: id(INTEGER) not null *1
                1: entry_date(TEXT)
                2: date_created(TEXT)
                3: last_modified(TEXT)
                4: title(TEXT)
                5: entry_body_id(INTEGER) not null
            entry_bodies:
                0: id(INTEGER) not null *1
                1: entry_id(INTEGER) not null
                2: body(TEXT)
            entry_tag:
                0: entry_id(INTEGER) not null
                1: tag_id(INTEGER) not null
            tags:
                0: id(INTEGER) not null *1
                1: name(TEXT)
        """
    conn = sqlite3.connect(path)
    if password != None:
        conn.execute('pragma key="{}"'.format(password))
    c = conn.cursor()
    c.execute("""CREATE TABLE entries (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        entry_date TEXT,
        date_created TEXT,
        last_modified TEXT,
        title TEXT,
        entry_body_id INTEGER NOT NULL,
        FOREIGN KEY("entry_body_id") REFERENCES "entry_bodies"("id")
    )""")

    c.execute("""CREATE TABLE entry_bodies (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        entry_id INTEGER NOT NULL,
        body TEXT,
        FOREIGN KEY("entry_id") REFERENCES "entries"("id")
    )""")

    c.execute("""CREATE TABLE tags (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )""")

    c.execute("""CREATE TABLE entry_tag (
        entry_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,
        FOREIGN KEY("entry_id") REFERENCES "entries"("id")
        FOREIGN KEY("tag_id") REFERENCES "tags"("id")
    )""")

    conn.commit()
    conn.close()
