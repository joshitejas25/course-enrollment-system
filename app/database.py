import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/enrollment.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            department TEXT NOT NULL,
            year INTEGER NOT NULL
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL UNIQUE,
            course_name TEXT NOT NULL,
            instructor TEXT NOT NULL,
            credits INTEGER NOT NULL,
            capacity INTEGER NOT NULL,
            prerequisite TEXT
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            enrollment_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'Enrolled',
            UNIQUE(student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students(id)
                ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id)
                ON DELETE CASCADE
        )
        """
    )

    connection.commit()
    connection.close()