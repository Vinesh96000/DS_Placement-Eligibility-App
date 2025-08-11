# app.py
import streamlit as st
import pandas as pd
import sqlite3
import joblib
import os
import sqlite3

DB_PATH = os.path.abspath("placement.db")
print(f"🔍 Using database file: {DB_PATH}")
print(f"📦 Database exists: {os.path.exists(DB_PATH)}")

# Optional: show tables in DB
conn = sqlite3.connect(DB_PATH)
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(f"📋 Tables in DB: {[t[0] for t in tables]}")
conn.close()


# Load the trained model
model = joblib.load("placement_model.pkl")  # change if filename is different

# --- Database Functions ---
def get_students():
    conn = sqlite3.connect("placement.db")
    df = pd.read_sql("SELECT student_id, name FROM Students", conn)
    conn.close()
    return df

def get_student_features(student_id):
    conn = sqlite3.connect("placement.db")
    query = """
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
JOIN SoftSkills ss ON s.student_id = ss.student_id
JOIN Placements p ON s.student_id = p.student_id
WHERE s.student_id = ?
"""

    print("DEBUG ID:", student_id)  # This will show in Streamlit logs
    df = pd.read_sql(query, conn, params=(int(student_id),))
    conn.close()
    print("DEBUG DF:", df)  # Show data before returning
    return df


# --- Streamlit UI ---
st.set_page_config(page_title="DS_Placement Eligibility app", page_icon="🎓", layout="centered")
st.title("DS_Placement Eligibility App")
st.write("Select a student to check placement eligibility based on database records.")

students_df = get_students()
student_choice = st.selectbox("Choose Student", students_df["name"].tolist())

if student_choice:
    student_id = students_df.loc[students_df["name"] == student_choice, "student_id"].values[0]
    features_df = get_student_features(student_id)

    if not features_df.empty:
        st.subheader("📌 Student Features")
        st.dataframe(features_df)

        if st.button("Predict Placement Eligibility"):
            try:
                prediction = model.predict(features_df)[0]
                probability = model.predict_proba(features_df)[0][1]

                st.success(f"Prediction: {'✅ Eligible' if prediction == 1 else '❌ Not Eligible'}")
                st.info(f"Confidence: {probability*100:.2f}%")
            except Exception as e:
                st.error(f"Prediction failed: {e}")
    else:
        st.warning("No feature data found for this student.")
