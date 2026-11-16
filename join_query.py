from db_connection import connect_db

conn = connect_db()
cursor = conn.cursor()

cursor.execute("""
SELECT
    e.emp_name,
    d.dept_name,
    e.salary
FROM employees e
JOIN departments d
ON e.dept_id = d.dept_id
""")

rows = cursor.fetchall()

for row in rows[:10]:
    print(row)

cursor.close()
conn.close()