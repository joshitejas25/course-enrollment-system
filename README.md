# CampusFlow — Course Enrollment Management System

CampusFlow is a menu-driven, terminal-based Course Enrollment Management System built with Python.

The application allows administrators to manage students, courses, and enrollments through a Rich-powered command-line interface. It stores data permanently using SQLite and exports records into a formatted Excel workbook.

## Features

### Student Management

- Add a student
- View all students
- Update student details
- Delete a student
- Validate email and phone number
- Prevent duplicate email addresses

### Course Management

- Add a course
- View all courses
- Update course details
- Delete a course
- Store course capacity and credits
- Store prerequisite course codes
- Prevent duplicate course codes

### Enrollment Management

- Enroll a student in a course
- View all enrollments
- Prevent duplicate enrollments
- Check whether the student exists
- Check whether the course exists
- Check prerequisite requirements
- Automatically enroll or waitlist students based on course capacity
- Drop an enrollment while preserving its history

### Dashboard

The dashboard displays:

- Total students
- Total courses
- Total enrollments
- Active enrollments
- Waitlisted students
- Dropped enrollments
- Available seats

### Excel Export

The application exports data into:

```text
exports/course_enrollment_report.xlsx
```

The workbook contains four worksheets:

1. `Students`
2. `Courses`
3. `Enrollments`
4. `Dashboard`

The Excel file includes formatted headers, automatic column widths, filters, and frozen header rows.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| SQLite | Local database storage |
| Rich | Attractive terminal UI and validated prompts |
| OpenPyXL | Excel workbook creation and formatting |
| Git | Version control |
| GitHub | Remote repository hosting |

## Requirements

- macOS
- Python 3.10 or newer
- Terminal
- Git
- Microsoft Excel, Apple Numbers, or another spreadsheet application

This project works well on a MacBook Air with an M3 chip because it uses Python and platform-independent libraries.

## Project Structure

```text
course-enrollment-system/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── exporter.py
│   ├── models.py
│   ├── repositories.py
│   ├── services.py
│   ├── ui.py
│   └── validators.py
│
├── data/
│   └── enrollment.db
│
├── exports/
│   └── course_enrollment_report.xlsx
│
├── tests/
│   └── test_services.py
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Application Architecture

CampusFlow follows a layered architecture.

```text
User
 │
 ▼
ui.py
Rich menus, prompts, tables, and messages
 │
 ▼
services.py
Business rules and validation flow
 │
 ▼
repositories.py
SQL queries and database operations
 │
 ▼
database.py
SQLite connection and table creation
```

Excel export follows a separate path:

```text
database.py
     │
     ▼
exporter.py
     │
     ▼
course_enrollment_report.xlsx
```

## Responsibility of Each Module

### `main.py`

This is the entry point of the application.

It:

1. Creates the database tables.
2. Displays the welcome message.
3. Starts the main menu.

```python
from app.database import create_tables
from app.ui import application_menu, show_welcome_message


def main():
    create_tables()
    show_welcome_message()
    application_menu()


if __name__ == "__main__":
    main()
```

### `database.py`

This module manages the SQLite database.

It contains:

- Database path
- Database connection function
- Table creation logic
- Foreign-key activation

It creates three tables:

- `students`
- `courses`
- `enrollments`

### `models.py`

This module defines Python data models using `dataclass`.

The models represent application entities in Python:

```python
Student
Course
```

A model makes records easier to work with than raw dictionaries or tuples.

### `repositories.py`

This module contains SQL operations.

Examples:

- Insert a student
- Select all students
- Update a course
- Delete a course
- Count enrolled students
- Insert an enrollment
- Retrieve dashboard statistics

The repository is responsible for communicating with SQLite.

### `services.py`

This module contains business logic.

Examples:

- Check whether a student exists
- Check whether a course exists
- Validate prerequisites
- Decide whether a student should be enrolled or waitlisted
- Prevent duplicate enrollment
- Coordinate repository functions

The service layer keeps business rules separate from the UI.

### `validators.py`

This module contains input validation functions.

Examples:

- Validate a name
- Validate an email address
- Validate a phone number
- Validate course credits
- Validate course capacity

Validation prevents incorrect data from entering the database.

### `ui.py`

This module controls the terminal interface.

It contains:

- Main menu
- Student menu
- Course menu
- Enrollment menu
- Rich tables
- Rich prompts
- Confirmation messages
- Error messages
- Dashboard display

The UI collects user input and calls the service layer.

### `exporter.py`

This module creates the Excel workbook.

It:

1. Reads database records.
2. Creates an Excel workbook.
3. Creates four worksheets.
4. Adds headers and rows.
5. Applies formatting.
6. Saves the workbook inside the `exports` directory.

## Database Design

### Students Table

| Column | Description |
|---|---|
| `id` | Unique student identifier |
| `name` | Student name |
| `email` | Unique student email |
| `phone` | Student phone number |
| `department` | Student department |
| `year` | Academic year |

### Courses Table

| Column | Description |
|---|---|
| `id` | Unique course identifier |
| `course_code` | Unique course code |
| `course_name` | Name of the course |
| `instructor` | Course instructor |
| `credits` | Number of credits |
| `capacity` | Maximum number of students |
| `prerequisite` | Required previous course |

### Enrollments Table

| Column | Description |
|---|---|
| `id` | Unique enrollment identifier |
| `student_id` | Foreign key referring to a student |
| `course_id` | Foreign key referring to a course |
| `enrollment_date` | Date and time of enrollment |
| `status` | `Enrolled`, `Waitlisted`, or `Dropped` |

## Database Relationship

Students and courses have a many-to-many relationship.

A student can enroll in many courses, and one course can contain many students.

The `enrollments` table resolves this relationship:

```text
Students 1 ────────< Enrollments >──────── 1 Courses
```

The foreign keys ensure that every enrollment belongs to an existing student and course.

## Enrollment Flow

```text
User selects a student
          │
          ▼
System checks whether the student exists
          │
          ▼
User selects a course
          │
          ▼
System checks whether the course exists
          │
          ▼
System checks prerequisite
          │
          ▼
System checks course capacity
          │
     ┌────┴────┐
     ▼         ▼
 Enrolled   Waitlisted
```

### Enrollment Rules

1. The student must exist.
2. The course must exist.
3. The student cannot enroll in the same course twice.
4. If the prerequisite is not satisfied, enrollment is rejected.
5. If seats are available, status becomes `Enrolled`.
6. If the course is full, status becomes `Waitlisted`.
7. Dropping an enrollment changes the status to `Dropped`.

## Installation on macOS

Open Terminal and move into the project directory:

```bash
cd course-enrollment-system
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Application

Make sure the virtual environment is active:

```bash
source .venv/bin/activate
```

Start the application:

```bash
python main.py
```

The application displays:

```text
1. Student Management
2. Course Management
3. Enrollment Management
4. View Dashboard
5. Export Data to Excel
6. Exit
```

## Exporting Data to Excel

From the main menu, choose:

```text
5. Export Data to Excel
```

The report is created at:

```text
exports/course_enrollment_report.xlsx
```

Open it on macOS with:

```bash
open exports/course_enrollment_report.xlsx
```

The workbook contains:

- All students
- All courses
- All enrollment records
- Dashboard statistics

## Testing the Application Manually

### Student Test

1. Add a student.
2. View students.
3. Update the student.
4. View the updated record.
5. Delete the student.
6. Confirm that the student is removed.

### Course Test

1. Add a course.
2. View courses.
3. Update the course.
4. View the updated record.
5. Delete the course.
6. Confirm that the course is removed.

### Enrollment Test

1. Create a student.
2. Create a course.
3. Enroll the student.
4. View enrollments.
5. Try enrolling the same student again.
6. Confirm that duplicate enrollment is rejected.
7. Drop the enrollment.
8. Confirm that the status changes to `Dropped`.

### Waitlist Test

1. Create a course with capacity `1`.
2. Add two students.
3. Enroll the first student.
4. Enroll the second student.
5. Confirm that the second student becomes `Waitlisted`.

### Excel Test

1. Add students.
2. Add courses.
3. Create enrollments.
4. Export the data.
5. Open the workbook.
6. Check all four worksheets.

## Error Handling

The application handles common errors such as:

- Duplicate student email
- Duplicate course code
- Invalid email
- Invalid phone number
- Invalid credits
- Invalid capacity
- Student not found
- Course not found
- Duplicate enrollment
- Enrollment not found
- Excel export failure

The purpose of error handling is to show a clear message instead of allowing the application to crash.

## Git Workflow

Initialize Git:

```bash
git init
```

Check project status:

```bash
git status
```

Add files:

```bash
git add .
```

Create the first commit:

```bash
git commit -m "chore: initialize course enrollment project"
```

Recommended commit history:

```text
chore: initialize course enrollment project
feat: add database schema
feat: implement student CRUD
feat: implement course CRUD
feat: add enrollment management
feat: add dashboard statistics
feat: add excel export
feat: improve input validation
docs: complete project README
test: verify core workflows
```

Rename the default branch:

```bash
git branch -M main
```

Connect the GitHub repository:

```bash
git remote add origin https://github.com/YOUR-USERNAME/course-enrollment-system.git
```

Push the project:

```bash
git push -u origin main
```

## Important Git Files

### `.gitignore`

The following files should not be uploaded:

```text
__pycache__/
*.py[cod]
.venv/
data/*.db
exports/*.xlsx
.DS_Store
```

The virtual environment is local to the computer and should not be committed to GitHub.

## Why SQLite Was Used

SQLite is suitable for this project because:

- It is included with Python.
- It does not require a separate database server.
- It stores data in a single local file.
- It supports SQL and relationships.
- It is simple to demonstrate during evaluation.

The database file is:

```text
data/enrollment.db
```

## Why Rich Was Used

Rich improves the terminal experience by providing:

- Colored text
- Tables
- Panels
- Validated prompts
- Clear success and error messages

Without Rich, the application would rely on plain `print()` and `input()` statements.

## Why OpenPyXL Was Used

OpenPyXL was used because it can:

- Create Excel workbooks
- Create worksheets
- Add rows and columns
- Apply fonts and colors
- Adjust column widths
- Freeze header rows
- Add filters
- Save `.xlsx` files

## Future Improvements

Possible future improvements include:

- Student login and administrator login
- Course search and filtering
- Automatic promotion from waitlist
- Course completion records
- Attendance management
- Grade management
- Export to CSV and PDF
- Graphical user interface
- Web-based version using Flask or Django
- Automated unit tests
- Database migration support

## Learning Outcomes

This project demonstrates:

- Python functions
- Modules and packages
- Classes and dataclasses
- Exception handling
- Input validation
- CRUD operations
- SQL and SQLite
- Primary keys
- Foreign keys
- Unique constraints
- Many-to-many relationships
- Rich terminal interfaces
- Excel workbook generation
- Git version control
- GitHub repository management
- Layered application architecture

## Author

Created by: `Tejas Joshi`

Project: Program-Based Learning — Week 1

Technology: Python

Project Name: CampusFlow Course Enrollment Management System