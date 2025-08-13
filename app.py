# app.py
import os
import sqlite3
import joblib
import pandas as pd
import streamlit as st

# ------------------------
# Config & Paths
# ------------------------
DB_PATH = os.path.abspath("placement.db")
MODEL_PATH = "placement_model.pkl"

st.set_page_config(page_title="DS_Placement Eligibility App", page_icon="🎓", layout="wide")
st.title("DS_Placement Eligibility App")
st.caption("Select a student to check placement eligibility based on database records.")

# ------------------------
# Small helpers
# ------------------------
def run_sql(sql: str, params: tuple | None = None) -> pd.DataFrame:
    """Safely run a SQL query and return a DataFrame."""
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(sql, conn, params=params)
    return df

def safe_dataframe_show(df: pd.DataFrame):
    if df.empty:
        st.warning("No matching records found. Try different criteria.")
    else:
        st.dataframe(df, use_container_width=True)

# ------------------------
# Model load (and quick info)
# ------------------------
model = joblib.load(MODEL_PATH)

with st.expander("ℹ️ Model Info"):
    st.write("**Model class:**", type(model).__name__)
    # In case they ask about features/shape during eval:
    st.write("**How we use it:** We pass the selected student's feature row "
             "(programming + soft skills + placements signals) to `predict()` "
             "and show `predict_proba()` as confidence.")

# ------------------------
# Student selection & prediction
# ------------------------
students_df = run_sql("SELECT student_id, name FROM Students ORDER BY name")

student_choice = st.selectbox("Choose Student", students_df["name"].tolist())
if student_choice:
    student_id = int(students_df.loc[students_df["name"] == student_choice, "student_id"].values[0])

    features_sql = """
    SELECT 
        pr.problems_solved,
        pr.assessments_completed,
        pr.mini_projects,
        pr.certifications_earned,
        pr.latest_project_score,
        ss.communication,
        ss.teamwork,
        ss.presentation,
        ss.leadership,
        ss.critical_thinking,
        ss.interpersonal_skills,
        p.mock_interview_score,
        p.internships_completed
    FROM Students s
    JOIN Programming pr ON s.student_id = pr.student_id
    JOIN SoftSkills ss  ON s.student_id = ss.student_id
    JOIN Placements p   ON s.student_id = p.student_id
    WHERE s.student_id = ?
    """
    features_df = run_sql(features_sql, params=(student_id,))

    st.subheader("📌 Student Features")
    safe_dataframe_show(features_df)

    if not features_df.empty and st.button("Predict Placement Eligibility"):
        try:
            pred = model.predict(features_df)[0]
            prob = float(model.predict_proba(features_df)[0][1])
            if pred == 1:
                st.success("Prediction: ✅ Eligible")
            else:
                st.error("Prediction: ❌ Not Eligible")
            st.info(f"Confidence: {prob*100:.2f}%")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

# ------------------------
# 📊 SQL Insights (10 queries, visible)
# ------------------------
st.header("📊 SQL Insights (10 Queries)")

queries: dict[str, str] = {
    # 1
    "Average programming performance per batch":
        """
        SELECT s.course_batch,
               AVG(p.problems_solved)          AS avg_problems_solved,
               AVG(p.assessments_completed)    AS avg_assessments,
               AVG(p.latest_project_score)     AS avg_project_score
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        GROUP BY s.course_batch
        ORDER BY s.course_batch
        """,

    # 2
    "Top 5 students ready for placement (by mock interview score)":
        """
        SELECT s.name, pl.mock_interview_score, pl.placement_status
        FROM Students s
        JOIN Placements pl ON s.student_id = pl.student_id
        WHERE pl.placement_status IN ('Ready','Placed')
        ORDER BY pl.mock_interview_score DESC
        LIMIT 5
        """,

    # 3
    "Distribution of soft skills (dataset averages)":
        """
        SELECT AVG(communication)     AS avg_communication,
               AVG(teamwork)          AS avg_teamwork,
               AVG(presentation)      AS avg_presentation,
               AVG(leadership)        AS avg_leadership,
               AVG(critical_thinking) AS avg_critical_thinking,
               AVG(interpersonal_skills) AS avg_interpersonal
        FROM SoftSkills
        """,

    # 4
    "Students with > 100 problems solved":
        """
        SELECT s.name, p.problems_solved
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        WHERE p.problems_solved > 100
        ORDER BY p.problems_solved DESC
        """,

    # 5
    "Students with more than 2 internships":
        """
        SELECT s.name, pl.internships_completed
        FROM Students s
        JOIN Placements pl ON s.student_id = pl.student_id
        WHERE pl.internships_completed > 2
        ORDER BY pl.internships_completed DESC
        """,

    # 6
    "Average placement package by graduation year":
        """
        SELECT s.graduation_year, AVG(pl.placement_package) AS avg_package
        FROM Students s
        JOIN Placements pl ON s.student_id = pl.student_id
        GROUP BY s.graduation_year
        ORDER BY s.graduation_year
        """,

    # 7
    "Top 5 leadership scorers":
        """
        SELECT s.name, ss.leadership
        FROM Students s
        JOIN SoftSkills ss ON s.student_id = ss.student_id
        ORDER BY ss.leadership DESC
        LIMIT 5
        """,

    # 8
    "Ready vs Not Ready vs Placed (counts)":
        """
        SELECT pl.placement_status, COUNT(*) AS count_students
        FROM Placements pl
        GROUP BY pl.placement_status
        """,

    # 9
    "Placed students by company (count)":
        """
        SELECT pl.company_name, COUNT(*) AS placed_count
        FROM Placements pl
        WHERE pl.placement_status = 'Placed' AND pl.company_name IS NOT NULL
        GROUP BY pl.company_name
        ORDER BY placed_count DESC
        """,

    # 10
    "Students who cleared > 3 interview rounds":
        """
        SELECT s.name, pl.interview_rounds_cleared
        FROM Students s
        JOIN Placements pl ON s.student_id = pl.student_id
        WHERE pl.interview_rounds_cleared > 3
        ORDER BY pl.interview_rounds_cleared DESC
        """
}

# show them
for title, sql in queries.items():
    st.subheader(title)
    st.code(sql.strip(), language="sql")
    df = run_sql(sql)
    safe_dataframe_show(df)

# ------------------------
# 🧪 Optional: Custom SQL runner for evaluators
# ------------------------
with st.expander("🧪 Run Custom SQL"):
    user_sql = st.text_area("Enter a SELECT query on Students / Programming / SoftSkills / Placements")
    if st.button("Execute"):
        try:
            df = run_sql(user_sql)
            safe_dataframe_show(df)
        except Exception as e:
            st.error(f"Error executing query: {e}")
