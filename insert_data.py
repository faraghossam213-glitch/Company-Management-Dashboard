import pandas as pd
from db_connection import connect_db

df = pd.read_csv("MOCK_DATA.csv")

conn = connect_db()
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO employees
        (emp_name, age, salary, hire_date, dept_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        row["emp_name"],
        int(row["age"]),
        float(row["salary"]),
        row["hire_date"],
        int(row["dept_id"])
    ))

conn.commit()

print("Data Inserted Successfully!")

cursor.close()
conn.close()