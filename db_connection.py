import psycopg2

def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="company_db",
        user="postgres",
        password="postgres"
    )
    return conn