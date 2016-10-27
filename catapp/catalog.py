import sqlite3
import os


db = None   # This variable is used for database connection later


# Open database connection and attach it to db variable
def open_database_connection(self):
    database_name = 'catalog.db'
    project_path = os.path.dirname(os.path.abspath(__file__))
    database_path = project_path + '/' + database_name
    self.db = sqlite3.connect(database_path)
    print("Connection to database opened")
