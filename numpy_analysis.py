import pandas as pd
import numpy as np
from db_connection import connect_db

conn = connect_db()

df = pd.read_sql("SELECT salary FROM employees", conn)

salaries = df["salary"].to_numpy()

print("Mean Salary:", np.mean(salaries))
print("Maximum Salary:", np.max(salaries))
print("Minimum Salary:", np.min(salaries))
print("Standard Deviation:", np.std(salaries))

conn.close()