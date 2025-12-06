from __future__ import annotations

import mysql.connector as mysql_conn

class Database:
    """

    Layer abstraksi untuk melakukan database operation
    Hanya digunakan untuk database interface developer
    Biasanya server dev and UI dev tidak perlu menggunakan class ini
    Walaupun itu, server/UI dev juga seharusnya tidak berinteraksi
    secara langsung dengan database, gunakan helper function dalam
    manager.py dan helper.py

    """
    DUPLICATE_ERRNO = 1062
    NOT_NULL_ERRNO = 1048

    def __init__(self):
        # Config for Abet's Linux machine
       # self.db = mysql_conn.connect(
       #     host = 'localhost',
       #     user = 'banking',
       #     password = 'password',
       #     database = 'banking'
       # )

        # Laragon defaults probably
        self.db = mysql_conn.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'banking'
        )

        self.cursor = self.db.cursor()

    def exec_query(self, query: str, val: tuple | None = None) -> None:
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)
    
    def exec_insert_query(self, query: str, val: tuple| None = None) -> int | None:
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)
        return self.cursor.lastrowid
    
    def fetch(self, query: str, val: tuple | None = None) -> list:
        self.cursor.execute(query, val)
        return self.cursor.fetchall()
    
    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

db = Database()
