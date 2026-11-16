import pandas as pd
from db_connection import connect_db

conn = connect_db()

query = """
SELECT
    d.dept_name,
    COUNT(*) AS employees,
    ROUND(AVG(salary),2) AS avg_salary,
    MAX(salary) AS max_salary,
    MIN(salary) AS min_salary
FROM employees e
JOIN departments d
ON e.dept_id = d.dept_id
GROUP BY d.dept_name
ORDER BY d.dept_name;
"""

df = pd.read_sql(query, conn)

print(df)

df.to_excel("company_dashboard_data.xlsx", index=False)

conn.close()

print("Excel File Created Successfully!")