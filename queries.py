import sqlite3
import pandas as pd

class DatabaseQueries:
    def __init__(self, db_name="placement.db"):
        self.db_name = db_name

    def run_query(self, query, params=None):
        with sqlite3.connect(self.db_name) as conn:
            return pd.read_sql_query(query, conn, params=params)

    def all_students(self):
        return self.run_query("SELECT * FROM Students")

    def top_programmers(self, min_problems=50):
        return self.run_query("""
        SELECT s.name, p.problems_solved
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        WHERE p.problems_solved > ?
        ORDER BY p.problems_solved DESC
        """, (min_problems,))

    def high_soft_skills(self, min_score=75):
        return self.run_query("""
        SELECT s.name, ss.communication, ss.teamwork
        FROM Students s
        JOIN SoftSkills ss ON s.student_id = ss.student_id
        WHERE ss.communication > ? AND ss.teamwork > ?
        """, (min_score, min_score))

    def avg_programming_per_batch(self):
        return self.run_query("""
        SELECT s.course_batch, AVG(p.problems_solved) AS avg_problems
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        GROUP BY s.course_batch
        """)

    def top5_ready_for_placement(self):
        return self.run_query("""
        SELECT s.name, pl.placement_status, p.problems_solved, ss.teamwork
        FROM Students s
        JOIN Placements pl ON s.student_id = pl.student_id
        JOIN Programming p ON s.student_id = p.student_id
        JOIN SoftSkills ss ON s.student_id = ss.student_id
        WHERE pl.placement_status = 'Ready'
        ORDER BY p.problems_solved DESC
        LIMIT 5
        """)

    # Add 5 more queries as per your doc...

if __name__ == "__main__":
    dq = DatabaseQueries()
    print(dq.all_students())
    print(dq.top_programmers())
    print(dq.high_soft_skills())
    print(dq.avg_programming_per_batch())
    print(dq.top5_ready_for_placement())
