from db_connection import connect_db

conn = connect_db()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO employees
(emp_name, age, salary, hire_date, dept_id)
VALUES
('Test Employee', 25, 18000, CURRENT_DATE, 1)
""")

conn.commit()

print("Employee Added Successfully!")

cursor.close()
conn.close()