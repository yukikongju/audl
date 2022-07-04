import sqlite3
import logging
import sys


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def execute_sql_query(conn, query):
    """ 
    Function that execute sql query to database from connection
    :param conn: Connection object
    :param query: sql query to be executed
    :return success_flag: True if query has been executed, else False
    """
    try: 
        cursor = conn.cursor()
        cursor.execute(query)
        return True
    except:
        logging.error("An error has occured when executing sql query")
        sys.exit(1)
        return False


def is_query_valid(query):
    """ 
    Function that check wether a SQL query is valid
    :param query: 
    :return success_flag: True if query has been executed, else False
    """
    pass


def main():
    database = "../database/audlDB.db"
    

if __name__ == "__main__":
    main()
    
