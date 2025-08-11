#!/usr/bin/env python3
"""
create_database.py
Create placement.db with all required tables matching data_generator.py
"""

import sqlite3


def create_tables(conn):
    """Create Students, Programming, SoftSkills, Placements tables."""
    cur = conn.cursor()

    # Students table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            email TEXT,
            phone TEXT,
            enrollment_year INTEGER,
            course_batch TEXT,
            city TEXT,
            graduation_year INTEGER
        )
    """)

    # Programming table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Programming (
            prog_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            language TEXT,
            problems_solved INTEGER,
            assessments_completed INTEGER,
            mini_projects INTEGER,
            certifications_earned INTEGER,
            latest_project_score INTEGER,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
    """)

    # SoftSkills table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS SoftSkills (
            soft_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            communication INTEGER,
            teamwork INTEGER,
            presentation INTEGER,
            leadership INTEGER,
            critical_thinking INTEGER,
            interpersonal_skills INTEGER,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
    """)

    # Placements table (now matches data_generator.py)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Placements (
            placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            mock_interview_score INTEGER,
            internships_completed INTEGER,
            placement_status TEXT,
            company_name TEXT,
            placement_package REAL,
            interview_rounds_cleared INTEGER,
            placement_date TEXT,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
    """)

    conn.commit()


def main():
    """Main entry to create DB."""
    conn = sqlite3.connect("placement.db")
    create_tables(conn)
    conn.close()


if __name__ == "__main__":
    main()
