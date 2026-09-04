from app.database import get_connection
from app.models import Course, Student


def add_student(student: Student):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO students (name, email, phone, department, year)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            student.name,
            student.email,
            student.phone,
            student.department,
            student.year,
        ),
    )

    connection.commit()
    student.id = cursor.lastrowid
    connection.close()

    return student


def get_all_students():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, name, email, phone, department, year
        FROM students
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    return [
        Student(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            phone=row["phone"],
            department=row["department"],
            year=row["year"],
        )
        for row in rows
    ]

def update_student(student_id, name, email, phone, department, year):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE students
        SET name = ?, email = ?, phone = ?, department = ?, year = ?
        WHERE id = ?
        """,
        (name, email, phone, department, year, student_id),
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0


def delete_student(student_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,),
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0


def add_course(course: Course):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO courses
        (course_code, course_name, instructor, credits, capacity, prerequisite)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            course.course_code,
            course.course_name,
            course.instructor,
            course.credits,
            course.capacity,
            course.prerequisite,
        ),
    )

    connection.commit()
    course.id = cursor.lastrowid
    connection.close()

    return course


def get_all_courses():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, course_code, course_name, instructor,
               credits, capacity, prerequisite
        FROM courses
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    return [
        Course(
            id=row["id"],
            course_code=row["course_code"],
            course_name=row["course_name"],
            instructor=row["instructor"],
            credits=row["credits"],
            capacity=row["capacity"],
            prerequisite=row["prerequisite"] or "",
        )
        for row in rows
    ]

def update_course(
    course_id,
    course_code,
    course_name,
    instructor,
    credits,
    capacity,
    prerequisite,
):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE courses
        SET course_code = ?,
            course_name = ?,
            instructor = ?,
            credits = ?,
            capacity = ?,
            prerequisite = ?
        WHERE id = ?
        """,
        (
            course_code,
            course_name,
            instructor,
            credits,
            capacity,
            prerequisite,
            course_id,
        ),
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0


def delete_course(course_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM courses WHERE id = ?",
        (course_id,),
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0


def get_student_by_id(student_id):
    connection = get_connection()

    student = connection.execute(
        """
        SELECT id, name, email, phone, department, year
        FROM students
        WHERE id = ?
        """,
        (student_id,),
    ).fetchone()

    connection.close()
    return student


def get_course_by_id(course_id):
    connection = get_connection()

    course = connection.execute(
        """
        SELECT id, course_code, course_name, instructor,
               credits, capacity, prerequisite
        FROM courses
        WHERE id = ?
        """,
        (course_id,),
    ).fetchone()

    connection.close()
    return course


def count_enrolled_students(course_id):
    connection = get_connection()

    count = connection.execute(
        """
        SELECT COUNT(*)
        FROM enrollments
        WHERE course_id = ?
        AND status = 'Enrolled'
        """,
        (course_id,),
    ).fetchone()[0]

    connection.close()
    return count


def add_enrollment(student_id, course_id, status):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO enrollments (student_id, course_id, status)
        VALUES (?, ?, ?)
        """,
        (student_id, course_id, status),
    )

    connection.commit()
    enrollment_id = cursor.lastrowid
    connection.close()

    return enrollment_id


def get_all_enrollments():
    connection = get_connection()

    enrollments = connection.execute(
        """
        SELECT
            enrollments.id,
            students.name AS student_name,
            courses.course_code,
            courses.course_name,
            enrollments.enrollment_date,
            enrollments.status
        FROM enrollments
        JOIN students ON students.id = enrollments.student_id
        JOIN courses ON courses.id = enrollments.course_id
        ORDER BY enrollments.id
        """
    ).fetchall()

    connection.close()
    return enrollments

def has_prerequisite(student_id, prerequisite_code):
    connection = get_connection()

    result = connection.execute(
        """
        SELECT enrollments.id
        FROM enrollments
        JOIN courses ON courses.id = enrollments.course_id
        WHERE enrollments.student_id = ?
        AND courses.course_code = ?
        AND enrollments.status = 'Enrolled'
        """,
        (student_id, prerequisite_code),
    ).fetchone()

    connection.close()

    return result is not None

def drop_enrollment(enrollment_id):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE enrollments
        SET status = 'Dropped'
        WHERE id = ?
        """,
        (enrollment_id,),
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0

def get_dashboard_statistics():
    connection = get_connection()

    total_students = connection.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_courses = connection.execute(
        "SELECT COUNT(*) FROM courses"
    ).fetchone()[0]

    total_enrollments = connection.execute(
        "SELECT COUNT(*) FROM enrollments"
    ).fetchone()[0]

    active_enrollments = connection.execute(
        """
        SELECT COUNT(*)
        FROM enrollments
        WHERE status = 'Enrolled'
        """
    ).fetchone()[0]

    waitlisted_students = connection.execute(
        """
        SELECT COUNT(*)
        FROM enrollments
        WHERE status = 'Waitlisted'
        """
    ).fetchone()[0]

    dropped_enrollments = connection.execute(
        """
        SELECT COUNT(*)
        FROM enrollments
        WHERE status = 'Dropped'
        """
    ).fetchone()[0]

    total_capacity = connection.execute(
        "SELECT COALESCE(SUM(capacity), 0) FROM courses"
    ).fetchone()[0]

    available_seats = total_capacity - active_enrollments

    connection.close()

    return {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "active_enrollments": active_enrollments,
        "waitlisted_students": waitlisted_students,
        "dropped_enrollments": dropped_enrollments,
        "available_seats": available_seats,
    }