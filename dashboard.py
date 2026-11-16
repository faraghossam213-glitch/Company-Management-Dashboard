import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import connect_db

# ======================================
# Page Configuration
# ======================================

st.set_page_config(
    page_title="Company Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("🏢 Company Management Dashboard")

st.caption(
    "Developed using PostgreSQL • Python • Pandas • Plotly • Streamlit"
)

st.markdown("---")
# ======================================
# Load Data
# ======================================

@st.cache_data
def load_data():

    conn = connect_db()

    query = """
    SELECT
        e.emp_id,
        e.emp_name,
        e.age,
        e.salary,
        e.hire_date,
        d.dept_name
    FROM employees e
    JOIN departments d
        ON e.dept_id = d.dept_id
    ORDER BY e.emp_id;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    df["hire_date"] = pd.to_datetime(df["hire_date"])

    return df


df = load_data()
# ======================================
# Sidebar Filters
# ======================================

st.sidebar.header("⚙️ Filters")

departments = ["All"] + sorted(df["dept_name"].unique())

selected_department = st.sidebar.selectbox(
    "🏢 Select Department",
    departments
)

search = st.sidebar.text_input(
    "🔍 Search Employee"
)

filtered_df = df.copy()

# Filter by department
if selected_department != "All":
    filtered_df = filtered_df[
        filtered_df["dept_name"] == selected_department
    ]

# Filter by employee name
if search:
    filtered_df = filtered_df[
        filtered_df["emp_name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]
    # ======================================
# KPI Cards
# ======================================

total_employees = len(filtered_df)
avg_salary = filtered_df["salary"].mean()
max_salary = filtered_df["salary"].max()
min_salary = filtered_df["salary"].min()

st.subheader("📈 Company Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👨‍💼 Total Employees",
        total_employees
    )

with col2:
    st.metric(
        "💰 Average Salary",
        f"${avg_salary:,.2f}"
    )

with col3:
    st.metric(
        "📈 Highest Salary",
        f"${max_salary:,.2f}"
    )

with col4:
    st.metric(
        "📉 Lowest Salary",
        f"${min_salary:,.2f}"
    )

st.markdown("---")
# ======================================
# Department Data
# ======================================

dept = (
    filtered_df
    .groupby("dept_name")
    .size()
    .reset_index(name="Employees")
)
# ======================================
# Bar Chart
# ======================================

# ======================================
# Charts Row 1
# ======================================

left, right = st.columns(2)

# ---------- Bar Chart ----------
with left:

    st.subheader("📊 Employees by Department")

    bar_fig = px.bar(
        dept,
        x="dept_name",
        y="Employees",
        text="Employees",
        color="dept_name",
        title="Employees by Department"
    )

    bar_fig.update_traces(
        textposition="outside"
    )

    bar_fig.update_layout(
        template="plotly_white",
        showlegend=False,
        xaxis_title="Department",
        yaxis_title="Employees"
    )

    st.plotly_chart(
        bar_fig,
        use_container_width=True
    )

# ---------- Pie Chart ----------
with right:

    st.subheader("🥧 Department Distribution")

    pie_fig = px.pie(
        dept,
        names="dept_name",
        values="Employees",
        hole=0.45,
        color="dept_name",
        title="Department Distribution"
    )

    pie_fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    pie_fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )

st.markdown("---")
# ======================================
# Charts Row 2
# ======================================

left2, right2 = st.columns(2)

# ---------- Salary Distribution ----------
with left2:

    st.subheader("💰 Salary Distribution")

    hist_fig = px.histogram(
        filtered_df,
        x="salary",
        nbins=10,
        color_discrete_sequence=["royalblue"],
        title="Salary Distribution"
    )

    hist_fig.update_layout(
        template="plotly_white",
        xaxis_title="Salary",
        yaxis_title="Employees"
    )

    st.plotly_chart(
        hist_fig,
        use_container_width=True
    )

# ---------- Hiring Trend ----------
with right2:

    st.subheader("📈 Hiring Trend")

    monthly = (
        filtered_df
        .groupby(
            filtered_df["hire_date"].dt.to_period("M")
        )
        .size()
        .reset_index(name="Employees")
    )

    monthly["hire_date"] = monthly["hire_date"].astype(str)

    line_fig = px.line(
        monthly,
        x="hire_date",
        y="Employees",
        markers=True,
        title="Employees Hired Per Month"
    )

    line_fig.update_traces(
        line=dict(width=3)
    )

    line_fig.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Employees"
    )

    st.plotly_chart(
        line_fig,
        use_container_width=True
    )

st.markdown("---")
# ======================================
# Download CSV
# ======================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Employees CSV",
    data=csv,
    file_name="employees.csv",
    mime="text/csv"
)

st.markdown("---")
# ======================================
# Employees Table
# ======================================

st.subheader("📋 Employees Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    height=450
)

st.caption(
    f"Showing {len(filtered_df)} employee(s)"
)
st.markdown("---")

st.caption(
    "© 2026 Company Dashboard | Built with PostgreSQL • Pandas • Plotly • Streamlit"
)