import sqlite3
import os
import decimal


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
                        name TEXT,
                        color VARCHAR(30),
                        size VARCHAR(10),
                        amount available INTEGER,
                        price REAL
                        )
                        """)
    db.commit()


def populate_test_data():
    """Populates shirt table with products with id range 1-250

    If id exists already, shirt won't be added
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


def get_shirts(order_by: str, order: str, limit: int, offset: int):
    """Fetches all shirts from database

    :return: All shirts with all information except id
    """
    # Since table name can't be given as a parameter, we will have to include it as a string
    # Thus we use a bit tacky way to make absolutely sure there can't be sql injections
    # We could also make unique execute cases for all alternatives but this way we can more easily modify query itself
    if order_by == "name":
        order_by = "name"
    elif order_by == "color":
        order_by = "color"
    elif order_by == "size":
        order_by = """CASE size
                    WHEN 'XS' THEN 0
                    WHEN 'S' THEN 1
                    WHEN 'M' THEN 2
                    WHEN 'L' THEN 3
                    WHEN 'XL' THEN 4
                    WHEN 'XXL' THEN 5
                    WHEN 'XXXL' THEN 6
                    END
                    """
    elif order_by == "amount":
        order_by = "amount"
    elif order_by == "price":
        order_by = "CAST(price AS REAL)"
    else:
        order_by = "name"

    # Same treatment for order
    if order == "asc":
        order = "ASC"
    elif order == "desc":
        order = "DESC"
    else:
        order = "ASC"

    cursor = db.cursor()
    cursor.execute("""SELECT *
                    FROM shirt
                    ORDER BY """ + order_by + " " + order + """
                    LIMIT ?
                    OFFSET ?
                    """, [limit, offset]
                   )
    return result_as_json(cursor)


def result_as_json(cursor):
    """Converts database cursor result to JSON.

    :param cursor: Result of SQL query
    :return: JSONified result
    """
    rows = [x for x in cursor.fetchall()]
    cols = [x[0] for x in cursor.description]
    results = []
    for row in rows:
        result = {}
        for prop, value in zip(cols, row):
            result[prop] = value
        results.append(result)
    return results
