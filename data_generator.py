import sqlite3
from faker import Faker
import random

fake = Faker()

class DatabaseSetup:
    def __init__(self, db_name="placement.db"):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute("""
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
        );
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Programming (
            programming_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            language TEXT,
            problems_solved INTEGER,
            assessments_completed INTEGER,
            mini_projects INTEGER,
            certifications_earned INTEGER,
            latest_project_score INTEGER,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        );
        """)

        self.cur.execute("""
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
        );
        """)

        self.cur.execute("""
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
        );
        """)
        self.conn.commit()

    def insert_fake_data(self, n=50):
        for _ in range(n):
            # Students
            name = fake.name()
            age = random.randint(20, 25)
            gender = random.choice(["Male", "Female", "Other"])
            email = fake.email()
            phone = fake.phone_number()
            enrollment_year = random.randint(2018, 2023)
            course_batch = random.choice(["Batch A", "Batch B", "Batch C"])
            city = fake.city()
            graduation_year = enrollment_year + 4

            self.cur.execute("""
            INSERT INTO Students (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year))

            student_id = self.cur.lastrowid

            # Programming
            self.cur.execute("""
            INSERT INTO Programming (student_id, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id, "Python",
                random.randint(0, 100),
                random.randint(0, 10),
                random.randint(0, 5),
                random.randint(0, 3),
                random.randint(50, 100)
            ))

            # Soft Skills
            self.cur.execute("""
            INSERT INTO SoftSkills (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                random.randint(50, 100),
                random.randint(50, 100),
                random.randint(50, 100),
                random.randint(50, 100),
                random.randint(50, 100),
                random.randint(50, 100)
            ))

            # Placements
            placement_status = random.choice(["Ready", "Not Ready", "Placed"])
            company_name = fake.company() if placement_status == "Placed" else None
            placement_package = round(random.uniform(3, 12), 2) if company_name else None
            self.cur.execute("""
            INSERT INTO Placements (student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                random.randint(50, 100),
                random.randint(0, 3),
                placement_status,
                company_name,
                placement_package,
                random.randint(0, 5),
                fake.date_this_year().isoformat() if company_name else None
            ))

        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = DatabaseSetup()
    db.create_tables()
    db.insert_fake_data(50)
    db.close()
