import mysql.connector as mysql_conn

class Database:
    def __init__(self):
        self.db = mysql_conn.connect(
            host = 'localhost',
            user = 'banking',
            password = 'password',
            database = 'banking'
        )

        self.cursor = self.db.cursor();
    
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
    
    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

def connect_db():
    return Database()