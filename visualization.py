import pandas as pd
import matplotlib.pyplot as plt
from db_connection import connect_db

# الاتصال بقاعدة البيانات
conn = connect_db()

# ==========================
# 1) Bar Chart
# ==========================

query = """
SELECT d.dept_name, COUNT(*) AS total
FROM employees e
JOIN departments d
ON e.dept_id = d.dept_id
GROUP BY d.dept_name
ORDER BY d.dept_name;
"""

df = pd.read_sql(query, conn)

plt.figure(figsize=(8, 5))

bars = plt.bar(df["dept_name"], df["total"])

plt.title("Employees by Department")
plt.xlabel("Department")
plt.ylabel("Number of Employees")

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.3,
        str(int(height)),
        ha="center"
    )

plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()


# ==========================
# 2) Pie Chart
# ==========================

plt.figure(figsize=(7, 7))

plt.pie(
    df["total"],
    labels=df["dept_name"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Employees Distribution by Department")
plt.tight_layout()
plt.show()


# ==========================
# 3) Histogram
# ==========================

salary_query = """
SELECT salary
FROM employees;
"""

salary_df = pd.read_sql(salary_query, conn)

plt.figure(figsize=(8, 5))

plt.hist(salary_df["salary"], bins=10)

plt.title("Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Number of Employees")

plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# ==========================
# 4) Line Chart
# ==========================

hire_query = """
SELECT hire_date
FROM employees;
"""

hire_df = pd.read_sql(hire_query, conn)

hire_df["hire_date"] = pd.to_datetime(hire_df["hire_date"])

hire_df["month"] = hire_df["hire_date"].dt.to_period("M")

monthly = hire_df.groupby("month").size()

plt.figure(figsize=(10, 5))

plt.plot(
    monthly.index.astype(str),
    monthly.values,
    marker="o"
)

plt.title("Employees Hired Per Month")
plt.xlabel("Month")
plt.ylabel("Number of Employees")

plt.xticks(rotation=45)

plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# غلق الاتصال
conn.close()
