# GenAI Usage Documentation

## Overview
Generative AI (Google Gemini) was used as a collaborative development and debugging assistant throughout the implementation and deployment of the **Job Application Tracker** web application for COP4751[cite: 3, 8]. All core architectural decisions, database schema design, and final code integrations were reviewed, tested, and verified locally.

## Areas of Assistance

### 1. Application Architecture & Backend Logic (`app.py`, `database.py`)
* **Routing & CRUD Operations**: Assisted in structuring modular Flask routes for managing companies, job listings, applications, and contacts.
* **SQL Query Formulation**: Provided guidance on writing parameterized SQL queries using `mysql-connector-python` to safely handle `INSERT`, `UPDATE`, `DELETE`, and multi-table `JOIN` operations while preventing SQL injection.
* **Job Match Ranking Algorithm**: Helped refine the scoring logic and SQL filtering criteria used to rank job opportunities based on user preferences and job attributes.

### 2. Frontend Templates (`templates/`)
* **UI Layout & Styling**: Assisted with Bootstrap grid layouts, responsive navigation bars, form validation markup, and clean table rendering across Jinja2 HTML templates.

### 3. Debugging & Version Control (Git / GitHub)
* **Error Resolution**: Helped diagnose and resolve Flask routing issues, MySQL connection errors, and template rendering bugs during local testing.
* **Git Workflow**: Provided troubleshooting commands to initialize the local repository, configure `.gitignore`, resolve unrelated merge histories, and sync local commits with the remote GitHub repository (`fnaj-000/job-application-tracker`).

### 4. Project Documentation (`README.md`)
* Assisted in drafting and formatting clear setup instructions, feature summaries, and technical documentation for repository submission.

## Verification & Academic Integrity
Every code snippet, SQL query, and configuration suggested by GenAI was manually inspected, adapted to fit the project's relational schema, and thoroughly tested against the local MySQL database to ensure accuracy and full understanding of the implementation.