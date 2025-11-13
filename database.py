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

    def exec_query(self, query, val=None):
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)
        self.db.commit()
    
    def exec_insert_query(self, query, val=None):
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)
        self.db.commit()
        return self.cursor.lastrowid
    
    def fetch(self, query, values):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def rollback(self):
        self.db.rollback()

def connect_db():
    return Database()