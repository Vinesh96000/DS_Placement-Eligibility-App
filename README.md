# Placement Eligibility Streamlit Application

## Project Overview
This project is a data-driven interactive web application built with Streamlit that allows placement teams to filter and shortlist students eligible for placements based on customizable criteria such as programming skills, soft skills, and placement readiness.

---

## Key Features
- Dynamic filtering of students based on input eligibility criteria  
- Uses synthetic student data generated with the Faker library  
- Stores data in a relational SQLite database with four related tables: Students, Programming, Soft Skills, and Placements  
- Object-Oriented Programming (OOP) principles for clean, modular code and database interaction  
- Ten SQL queries for insightful analytics (e.g., top performers, average scores per batch)  
- Interactive dashboards and tables for real-time decision-making  

---

## Technologies Used
- Python  
- Streamlit  
- Faker (for synthetic data generation)  
- SQLite (relational database)  
- SQL (for data queries and insights)  
- Object-Oriented Programming (OOP)  

---

## Dataset Schema

| Table           | Description                                  |
|-----------------|----------------------------------------------|
| Students        | Student personal and enrollment details     |
| Programming     | Programming performance metrics              |
| Soft Skills     | Scores for communication, teamwork, etc.    |
| Placements      | Placement readiness and outcomes             |

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/placement-eligibility-app.git
   cd placement-eligibility-app
