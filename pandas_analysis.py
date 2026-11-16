import pandas as pd
from db_connection import connect_db

conn = connect_db()

df = pd.read_sql("SELECT * FROM employee_details", conn)

print(df.head())

print("\nAverage Salary:")
print(df["salary"].mean())

print("\nMaximum Salary:")
print(df["salary"].max())

print("\nMinimum Salary:")
print(df["salary"].min())

print("\nEmployees in each department:")
print(df["dept_name"].value_counts())

conn.close()