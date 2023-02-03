import sqlite3
import os


class TinySQL:
    def __init__(self, db_name):
        self.is_new_db = not os.path.exists(db_name)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mytable (textfield TEXT)''')
        self.conn.commit()

    def update_row(self, index, new_value):
        try:
            self.cursor.execute(f'UPDATE mytable SET textfield = "{new_value}" WHERE rowid = {index}')
            self.conn.commit()
        except Exception as error:
            pass

    def insert_row(self, value):
        try:
            self.cursor.execute(f'INSERT INTO mytable (textfield) VALUES ("{value}")')
            self.conn.commit()
        except Exception as error:
            pass

    def read_all_rows(self):
        try:
            self.cursor.execute("SELECT * FROM mytable")
            data = self.cursor.fetchall()
            result = [x[0] for x in data]
            return result
        except Exception as error:
            return []
