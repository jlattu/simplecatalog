import sqlite3
import os

db = None   # This variable is used for database connection later
project_path = os.path.dirname(os.path.abspath(__file__))


def open_database_connection(self):
    """Open database connection and attach it to db variable.

    Also creates table for shirts if it doesn't exists yet.
    :param self:
    :return: Nothing
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
    """Populates shirt table with products. Test data file has 500 rows as of writing this.

    If id exists already, shirt won't be added.
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
        print(str(not_added) + ' shirts were not added because products with same id existed already')
    db.commit()
    return len(sql_commands) - 1 - not_added


def get_shirts(name: str, order_by: str, order: str, limit: int, offset: int):
    """"Fetches all shirts from database

    :param name: Searches for results beginning with this (everything if NULL)
    :param order_by: Ordering key (e.g. name or price)
    :param order: Ascending or descending
    :param limit: How many results we will get with one query
    :param offset: Starting from n:th result
    :return: All shirts with all information
    """
    # Since table name can't be given as a parameter, we will have to include it as a string
    # Thus we use a bit tacky way to make absolutely sure there can't be sql injections
    # We could also make unique execute cases for all alternatives but this way we can more easily modify query itself
    # (For most stating them again is probably useless)
    if order_by == "id":
        order_by == "id"
    elif order_by == "name":
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

    # Same treatment for order (asc or desc)
    if order == "asc":
        order = "ASC"
    elif order == "desc":
        order = "DESC"
    else:
        order = "ASC"

    # Add % at the end of parameter so search will be conducted for names starting with xyz
    name_begins = name + '%'

    cursor = db.cursor()
    cursor.execute("""SELECT *
                    FROM shirt
                    WHERE name LIKE ?
                    ORDER BY """ + order_by + " " + order + """
                    LIMIT ?
                    OFFSET ?
                    """, [name_begins, limit, offset]
                   )
    return result_as_json(cursor)


def get_shirt_count(name: str = ""):
    """Gets amount of all shirts possible to get with used search parameter.

    Main purpose is to help show right amount of pages for pagination.
    :param name: Searches for results beginning with this (everything if NULL)
    :return: Amount of rows
    """
    name_begins = name + '%'
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(id) FROM shirt WHERE name LIKE ?", [name_begins])
    return cursor.fetchone()[0]


def add_shirt(name: str, color: str, size: str, amount: int, price: float):
    """Adds new shirt to database. Unique id is given automatically.

    :param name: Name of the shirt
    :param color: Color of the shirt
    :param size: Size of the shirt
    :param amount: Amount of shirts
    :param price: Price of the shirt
    :return: Nothing
    """
    cursor = db.cursor()
    cursor.execute("""INSERT INTO shirt (name, color, size, amount, price)
                    VALUES (?, ?, ?, ?, ?)
                    """, [name, color, size, amount, price]
                   )
    db.commit()
    return


def update_shirt(shirt_id: int, name: str, color: str, size: str, amount: int, price: float):
    """Updates shirt with new information

    :param shirt_id: Id of the shirt (this can't be changed)
    :param name: Name of the shirt
    :param color: Color of the shirt
    :param size: Size of the shirt
    :param amount: Amount of shirts
    :param price: Price of the shirt
    :return: Nothing
    """
    cursor = db.cursor()
    cursor.execute("""UPDATE shirt
                    SET name = ?, color = ?, size = ?,
                    amount = ?, price = ?
                    WHERE id = ?
                    """, [name, color, size, amount, price, shirt_id]
                   )
    db.commit()
    return


def delete_shirt(shirt_id: int):
    """Adds new shirt to database

    :param shirt_id: Name of the shirt
    :return: Nothing
    """
    cursor = db.cursor()
    cursor.execute("""DELETE FROM shirt
                    WHERE id = ?
                    """, [shirt_id]
                   )
    db.commit()


def delete_all_shirts():
    """Deletes all shirts from the database

    :return: Nothing left to return
    """
    cursor = db.cursor()
    cursor.execute("""DELETE FROM shirt
                        """
                   )
    db.commit()


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
