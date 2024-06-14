import sqlite3

DATABASE_NAME = 'pwd_manager.db'

def connect():
    """
    Create a database connection to an SQLite database.

    Returns:
        sqlite3.Connection: The connection object to the SQLite database.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        print(e)
    return conn

def check_table():
    """
    Check if the PASSWORDS table exists, and create it if it doesn't.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    connection = connect()
    exists = False  
    create_table = """CREATE TABLE IF NOT EXISTS PASSWORDS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                SERVICE varchar NOT NULL, 
                USERNAME varchar,
                KEY BLOB
        );"""
    check_table = """SELECT name FROM sqlite_master WHERE type='table'
                AND name='PASSWORDS';"""
    
    cursor = connection.cursor()
    listOfTables = cursor.execute(check_table).fetchall()
    if listOfTables != []:
        exists = True
    cursor.execute(create_table)
    connection.commit()
    connection.close()
    return exists

def update_record(service, username, key):
    """
    Update the password record for a given service and username.

    Args:
        service (str): The name of the service.
        username (str): The username for the service.
        key (bytes): The encrypted password.

    Returns:
        bool: True if the record was updated, False if the record doesn't exist.
    """
    if len(get_record(service, username)) <= 0:
        print("The record doesn't exist!")
        return False
    update_statement = 'UPDATE PASSWORDS SET KEY=? WHERE SERVICE = ? AND USERNAME = ?'
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(update_statement, (key, service, username,))
    connection.commit()
    connection.close()
    return True

def save_record(service, username, key):
    """
    Save a new password record for a given service and username.

    Args:
        service (str): The name of the service.
        username (str): The username for the service.
        key (bytes): The encrypted password.

    Returns:
        bool: True if the record was saved, False if the record already exists.
    """
    if len(get_record(service, username)) > 0:
        print("The record already exists!")
        return False
    statement = 'INSERT INTO PASSWORDS(SERVICE, USERNAME, KEY) VALUES(?, ?, ?);'
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(statement, (service, username, key))
    connection.commit()
    connection.close()
    return True

def delete_record(service, username):
    """
    Delete a password record for a given service and username.

    Args:
        service (str): The name of the service.
        username (str): The username for the service.
    """
    statement = 'DELETE FROM PASSWORDS WHERE SERVICE = ? AND USERNAME = ?'
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(statement, (service, username,))
    connection.commit()
    connection.close()

def get_record(service, username):
    """
    Retrieve a password record for a given service and username.

    Args:
        service (str): The name of the service.
        username (str): The username for the service.

    Returns:
        list: The password record(s) for the given service and username.
    """
    statement = "SELECT KEY FROM PASSWORDS WHERE USERNAME=? AND SERVICE=?;"
    if username == "":
        statement = "SELECT KEY,USERNAME FROM PASSWORDS WHERE SERVICE=?;"
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(statement, (username, service))
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_all_records():
    """
    Retrieve all password records from the database.

    Returns:
        list: A list of all password records.
    """
    statement = "SELECT SERVICE,USERNAME,KEY FROM PASSWORDS;"
    connection = connect()
    connection.row_factory = factory_dict
    cursor = connection.cursor()
    cursor.execute(statement)
    rows = cursor.fetchall()
    connection.close()
    return rows

def factory_dict(cursor, row):
    """
    Convert a SQLite row to a dictionary.

    Args:
        cursor (sqlite3.Cursor): The cursor object.
        row (sqlite3.Row): The row to convert.

    Returns:
        dict: The row data as a dictionary.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
