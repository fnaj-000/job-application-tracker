import mysql.connector

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Root1234!',
        database='job_tracker'
    )