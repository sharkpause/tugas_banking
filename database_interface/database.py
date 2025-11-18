import mysql.connector as mysql_conn

class Database:
    DUPLICATE_ERRNO = 1062
    NOT_NULL_ERRNO = 1048

    def __init__(self):
        self.db = mysql_conn.connect(
            host = 'localhost',
            user = 'banking',
            password = 'password',
            database = 'banking'
        )

        self.cursor = self.db.cursor()

    def exec_query(self, query: str, val: tuple = None) -> None:
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)
    
    def exec_insert_query(self, query: str, val: tuple = None) -> int:
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)
        return self.cursor.lastrowid
    
    def fetch(self, query: str, val: tuple = None) -> list:
        self.cursor.execute(query, val)
        return self.cursor.fetchall()
    
    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

db = Database()