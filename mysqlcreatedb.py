import mysql.connector

# Connect to MySQL
def create_connection():
    return mysql.connector.connect(
        host="localhost",  # or your MySQL host
        user="britt",       # your MySQL username
        password="dougfunny",       # your MySQL password
        database="libraryManagementdb"
    )