import MySQLdb
from MySQLdb import Error

def create_connection():
    try:
        connection = MySQLdb.connect(
            host='localhost',          
            user='root',          
            password='',  
            database='mikmikmom'   
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
