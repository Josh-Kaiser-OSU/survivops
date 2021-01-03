# Sources:
# https://www.mysqltutorial.org/python-mysql-query/
# https://www.mysqltutorial.org/python-connecting-mysql-databases/


import mysql.connector
from mysql.connector import Error


def connect_to_database():
    """
    Connect to a MySQL database.
    :return connection: A MySQLConnection object
    """

    config = {
        "user": "root",
        "password": "root",
        "host": "db",
        "port": "3306",
        "database": "survivops"
    }

    connection = None
    try:
        connection = mysql.connector.connect(**config)
        if connection is not None and connection.is_connected():
            print("Connected to the MySQL database.")
            return connection
    
    except Error as e:
        print(e)


def execute_query(db_connection = None, query = None, query_params = ()):
    """
    Execute the given SQL query on the given MySQLConnection object.

    :param db_connection: A MySQLConnection object created by connect_to_database()
    :param query: A string containing the SQL query
    :param query_params: Parameters for the query

    :return cursor: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects
    Run .fetchall() or .fetchone() on the cursor to actually access the results.
    """

    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("The query is empty! Please provide a SQL query.")
        return None

    print("Executing %s with %s" % (query, query_params))

    # Create a cursor to execute the query. Why? Because apparently they optimize execution by retaining a reference according to PEP0249
    cursor = db_connection.cursor()

    """
    params = tuple()
    # Create a tuple of parameters to send with the query
    for q in query_params:
        params = params + (q)
    """
    #TODO: Sanitize the query before executing it

    cursor.execute(query, query_params)

    # Commit any changes to the database
    db_connection.commit()
    return cursor
