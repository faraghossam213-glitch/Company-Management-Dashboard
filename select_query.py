from db_connection import connect_db

conn = connect_db()
cursor = conn.cursor()

cursor.execute("SELECT * FROM employees")

rows = cursor.fetchall()

for row in rows[:10]:
    print(row)

cursor.close()
conn.close()