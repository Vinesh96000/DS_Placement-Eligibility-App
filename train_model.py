# train_model.py
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. Connect to database
conn = sqlite3.connect("placement.db")

# 2. Load data from DB (join Students, Programming, SoftSkills, Placements)
query = """
SELECT 
    s.student_id,
    p.language,
    p.problems_solved,
    p.assessments_completed,
    p.mini_projects,
    p.certifications_earned,
    p.latest_project_score,
    ss.communication,
    ss.teamwork,
    ss.presentation,
    ss.leadership,
    ss.critical_thinking,
    ss.interpersonal_skills,
    pl.mock_interview_score,
    pl.internships_completed,
    pl.placement_status
FROM Students s
JOIN Programming p ON s.student_id = p.student_id
JOIN SoftSkills ss ON s.student_id = ss.student_id
JOIN Placements pl ON s.student_id = pl.student_id
"""
df = pd.read_sql_query(query, conn)
conn.close()

# 3. Prepare target variable (binary classification: 1 = Ready/Placed, 0 = Not Ready)
df["target"] = df["placement_status"].apply(lambda x: 1 if x in ["Ready", "Placed"] else 0)
df = df.drop(columns=["placement_status", "language", "student_id"])  # remove non-numeric cols

# 4. Split features/target
X = df.drop(columns=["target"])
y = df["target"]

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluate model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 8. Save the model
joblib.dump(model, "placement_model.pkl")
print("Model saved as placement_model.pkl")
