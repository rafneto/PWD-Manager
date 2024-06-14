import sqlite3

DATABASE_NAME = 'pwd_manager.db'

def connect():
    """ create a database connection to an SQLite database """
    conn = None
    try:
        conn=sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        print(e)
    return conn

def check_table():
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
    if len(get_record(service, username)) <= 0:
        print("The record does't exist!")
        return False
    update_statement = 'UPDATE PASSWORDS SET KEY=? WHERE SERVICE = ? AND USERNAME = ?'
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(update_statement, (key, service, username,))
    connection.commit()
    connection.close()
    return True

def save_record(service, username, key):
    if len(get_record(service, username)) > 0:
        print("The record already exists!")
        return False
    statement = 'INSERT INTO PASSWORDS(SERVICE, USERNAME, KEY) VALUES("' + service + '","' + username + '","' + key + '");'
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    connection.close()
    return True

def delete_record(service, username):
    statement = 'DELETE FROM PASSWORDS WHERE SERVICE = ? AND USERNAME = ?'
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(statement, (service, username,))
    connection.commit()
    connection.close()
    
def get_record(service, username):
    statement = "SELECT KEY FROM PASSWORDS WHERE USERNAME='" + username + "' AND SERVICE='" + service + "';"
    if username == "":
        statement = "SELECT KEY,USERNAME FROM PASSWORDS WHERE SERVICE='" + service + "';"
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(statement)
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_all_records():
    statement = "SELECT SERVICE,USERNAME,KEY FROM PASSWORDS;"
    connection = connect()
    connection.row_factory = factory_dict
    cursor = connection.cursor()
    cursor.execute(statement)
    rows = cursor.fetchall()
    connection.close()
    return rows

def factory_dict(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
    