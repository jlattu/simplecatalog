import sqlite3
import os


db = None   # This variable is used for database connection later
project_path = os.path.dirname(os.path.abspath(__file__))


def open_database_connection(self):
    """Open database connection and attach it to db variable

    Also creates table for shirts if it doesn't exists yet
    :param self:
    :return:
    """
    database_name = 'catalog.db'
    database_path = project_path + '/' + database_name
    self.db = sqlite3.connect(database_path)
    print("Connection to database opened")

    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS shirt (
                        id INTEGER PRIMARY KEY,
                        shirt_name TEXT,
                        color VARCHAR(30),
                        shirt_size VARCHAR(10),
                        amount available INTEGER,
                        price REAL
                        )
                        """)
    db.commit()


def populate_test_data():
    """Populates shirt table with products with ID range 1-250

    If ID exists already, shirt won't be added
    :return: Number of shirts added to database
    """
    shirt_data_name = 'shirt_data.sql'
    shirt_path = project_path + '/' + shirt_data_name

    opened_file = open(shirt_path, 'r', encoding='utf-8')
    sql_file = opened_file.read()
    opened_file.close()
    sql_commands = sql_file.split(';')

    cursor = db.cursor()
    not_added = 0
    for command in sql_commands:
        try:
            cursor.execute(command)
        except sqlite3.Error:
            not_added += 1
    if not_added > 0:
        print(str(not_added) + ' shirts were not added because products with same ID existed already')
    db.commit()
    return len(sql_commands) - 1 - not_added
