import sqlite3
from app.models import Course, Student
from app.repositories import (
    add_course,
    add_enrollment,
    add_student,
    count_enrolled_students,
    delete_course,
    delete_student,
    drop_enrollment,
    get_all_courses,
    get_all_enrollments,
    get_all_students,
    get_course_by_id,
    get_dashboard_statistics,
    get_student_by_id,
    has_prerequisite,
    update_course,
    update_student,
)
from app.validators import (
    validate_capacity,
    validate_credits,
    validate_email,
    validate_name,
    validate_phone,
)

def register_student(
    name,
    email,
    phone,
    department,
    year,
):
    validations = [
        validate_name(name),
        validate_email(email),
        validate_phone(phone),
    ]

    for is_valid, message in validations:
        if not is_valid:
            return None, message

    student = Student(
        name=name,
        email=email,
        phone=phone,
        department=department,
        year=year,
    )

    return add_student(student), ""

def list_students():
    return get_all_students()


def edit_student(
    student_id,
    name,
    email,
    phone,
    department,
    year,
):
    return update_student(
        student_id,
        name,
        email,
        phone,
        department,
        year,
    )


def remove_student(student_id):
    return delete_student(student_id)


def register_course(
    course_code,
    course_name,
    instructor,
    credits,
    capacity,
    prerequisite,
):
    credits_valid, credits_message = validate_credits(credits)

    if not credits_valid:
        return None, credits_message

    capacity_valid, capacity_message = validate_capacity(capacity)

    if not capacity_valid:
        return None, capacity_message

    course = Course(
        course_code=course_code,
        course_name=course_name,
        instructor=instructor,
        credits=credits,
        capacity=capacity,
        prerequisite=prerequisite,
    )

    return add_course(course), ""



def list_courses():
    return get_all_courses()

def edit_course(
    course_id,
    course_code,
    course_name,
    instructor,
    credits,
    capacity,
    prerequisite,
):
    return update_course(
        course_id,
        course_code,
        course_name,
        instructor,
        credits,
        capacity,
        prerequisite,
    )


def remove_course(course_id):
    return delete_course(course_id)



def enroll_student(student_id, course_id):
    student = get_student_by_id(student_id)

    if student is None:
        return False, "Student not found."

    course = get_course_by_id(course_id)

    if course is None:
        return False, "Course not found."

    prerequisite = course["prerequisite"]

    if prerequisite:
        prerequisite_exists = has_prerequisite(
            student_id,
            prerequisite,
        )

        if not prerequisite_exists:
            return (
                False,
                f"Student must first enroll in {prerequisite}.",
            )

    enrolled_count = count_enrolled_students(course_id)

    if enrolled_count >= course["capacity"]:
        status = "Waitlisted"
    else:
        status = "Enrolled"

    try:
        add_enrollment(
            student_id,
            course_id,
            status,
        )
    except sqlite3.IntegrityError:
        return (
            False,
            "Student is already registered for this course.",
        )

    return True, f"Student successfully added with status: {status}"



def list_enrollments():
    return get_all_enrollments()

def remove_enrollment(enrollment_id):
    return drop_enrollment(enrollment_id)

def get_dashboard():
    return get_dashboard_statistics()