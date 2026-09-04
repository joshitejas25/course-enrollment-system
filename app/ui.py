import sqlite3

from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

from app.exporter import export_data_to_excel
from app.services import (
    edit_course,
    edit_student,
    enroll_student,
    get_dashboard,
    list_courses,
    list_enrollments,
    list_students,
    register_course,
    register_student,
    remove_course,
    remove_enrollment,
    remove_student,
)


console = Console()


def show_welcome_message():
    console.print("\n[bold cyan]Welcome to CampusFlow[/bold cyan]\n")


def show_student_table(students):
    if not students:
        console.print("[yellow]No students found.[/yellow]")
        return

    table = Table(title="Students")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Email", style="yellow")
    table.add_column("Department", style="magenta")
    table.add_column("Year", justify="center")

    for student in students:
        table.add_row(
            str(student.id),
            student.name,
            student.email,
            student.department,
            str(student.year),
        )

    console.print(table)


def show_course_table(courses):
    if not courses:
        console.print("[yellow]No courses found.[/yellow]")
        return

    table = Table(title="Courses")
    table.add_column("ID", style="cyan")
    table.add_column("Code", style="green")
    table.add_column("Course Name", style="yellow")
    table.add_column("Instructor", style="magenta")
    table.add_column("Credits", justify="center")
    table.add_column("Capacity", justify="center")
    table.add_column("Prerequisite", style="blue")

    for course in courses:
        table.add_row(
            str(course.id),
            course.course_code,
            course.course_name,
            course.instructor,
            str(course.credits),
            str(course.capacity),
            course.prerequisite or "None",
        )

    console.print(table)


def show_enrollment_table(enrollments):
    if not enrollments:
        console.print("[yellow]No enrollments found.[/yellow]")
        return

    table = Table(title="Enrollments")
    table.add_column("ID", style="cyan")
    table.add_column("Student", style="green")
    table.add_column("Course Code", style="yellow")
    table.add_column("Course Name", style="magenta")
    table.add_column("Date", style="blue")
    table.add_column("Status", style="bold")

    for enrollment in enrollments:
        status = enrollment["status"]
        status_style = "green" if status == "Enrolled" else "yellow"

        table.add_row(
            str(enrollment["id"]),
            enrollment["student_name"],
            enrollment["course_code"],
            enrollment["course_name"],
            enrollment["enrollment_date"],
            f"[{status_style}]{status}[/{status_style}]",
        )

    console.print(table)


def add_student_menu():
    console.print("\n[bold green]Add New Student[/bold green]")

    name = Prompt.ask("Student name")
    email = Prompt.ask("Email")
    phone = Prompt.ask("Phone number")
    department = Prompt.ask("Department")
    year = IntPrompt.ask(
        "Academic year",
        choices=["1", "2", "3", "4"],
    )

    try:
        student, message = register_student(
            name=name,
            email=email,
            phone=phone,
            department=department,
            year=year,
        )

        if student is None:
            console.print(f"[bold red]{message}[/bold red]")
        else:
            console.print(
                f"[bold green]Student added successfully with ID "
                f"{student.id}.[/bold green]"
            )

    except sqlite3.IntegrityError:
        console.print(
            "[bold red]A student with this email already exists.[/bold red]"
        )


def update_student_menu():
    console.print("\n[bold blue]Update Student[/bold blue]")

    student_id = IntPrompt.ask("Student ID")
    name = Prompt.ask("New name")
    email = Prompt.ask("New email")
    phone = Prompt.ask("New phone number")
    department = Prompt.ask("New department")
    year = IntPrompt.ask(
        "New academic year",
        choices=["1", "2", "3", "4"],
    )

    try:
        updated = edit_student(
            student_id,
            name,
            email,
            phone,
            department,
            year,
        )

        if updated:
            console.print("[green]Student updated successfully.[/green]")
        else:
            console.print("[yellow]Student ID not found.[/yellow]")

    except sqlite3.IntegrityError:
        console.print(
            "[bold red]That email already belongs to another student.[/bold red]"
        )


def delete_student_menu():
    console.print("\n[bold red]Delete Student[/bold red]")

    student_id = IntPrompt.ask("Student ID")
    confirmation = Prompt.ask(
        "Type DELETE to confirm",
        choices=["DELETE", "CANCEL"],
    )

    if confirmation == "DELETE":
        deleted = remove_student(student_id)

        if deleted:
            console.print("[green]Student deleted successfully.[/green]")
        else:
            console.print("[yellow]Student ID not found.[/yellow]")
    else:
        console.print("[yellow]Deletion cancelled.[/yellow]")


def student_menu():
    while True:
        console.print("\n[bold cyan]Student Management[/bold cyan]")
        console.print("1. Add student")
        console.print("2. View students")
        console.print("3. Update student")
        console.print("4. Delete student")
        console.print("5. Back")

        choice = Prompt.ask(
            "Choose an option",
            choices=["1", "2", "3", "4", "5"],
        )

        if choice == "1":
            add_student_menu()
        elif choice == "2":
            show_student_table(list_students())
        elif choice == "3":
            update_student_menu()
        elif choice == "4":
            delete_student_menu()
        else:
            break


def add_course_menu():
    console.print("\n[bold green]Add New Course[/bold green]")

    course_code = Prompt.ask("Course code")
    course_name = Prompt.ask("Course name")
    instructor = Prompt.ask("Instructor")
    credits = IntPrompt.ask(
        "Credits",
        choices=["1", "2", "3", "4", "5", "6"],
    )
    capacity = IntPrompt.ask("Maximum capacity")
    prerequisite = Prompt.ask(
        "Prerequisite course code",
        default="None",
    )

    if prerequisite.lower() == "none":
        prerequisite = ""

    try:
        course, message = register_course(
            course_code=course_code,
            course_name=course_name,
            instructor=instructor,
            credits=credits,
            capacity=capacity,
            prerequisite=prerequisite,
        )

        if course is None:
            console.print(f"[bold red]{message}[/bold red]")
        else:
            console.print(
                f"[bold green]Course added successfully with ID "
                f"{course.id}.[/bold green]"
            )

    except sqlite3.IntegrityError:
        console.print(
            "[bold red]A course with this code already exists.[/bold red]"
        )


def update_course_menu():
    console.print("\n[bold blue]Update Course[/bold blue]")

    course_id = IntPrompt.ask("Course ID")
    course_code = Prompt.ask("New course code")
    course_name = Prompt.ask("New course name")
    instructor = Prompt.ask("New instructor")
    credits = IntPrompt.ask(
        "New credits",
        choices=["1", "2", "3", "4", "5", "6"],
    )
    capacity = IntPrompt.ask("New capacity")
    prerequisite = Prompt.ask(
        "New prerequisite course code",
        default="None",
    )

    if prerequisite.lower() == "none":
        prerequisite = ""

    try:
        updated = edit_course(
            course_id,
            course_code,
            course_name,
            instructor,
            credits,
            capacity,
            prerequisite,
        )

        if updated:
            console.print("[green]Course updated successfully.[/green]")
        else:
            console.print("[yellow]Course ID not found.[/yellow]")

    except sqlite3.IntegrityError:
        console.print(
            "[bold red]That course code already exists.[/bold red]"
        )


def delete_course_menu():
    console.print("\n[bold red]Delete Course[/bold red]")

    course_id = IntPrompt.ask("Course ID")
    confirmation = Prompt.ask(
        "Type DELETE to confirm",
        choices=["DELETE", "CANCEL"],
    )

    if confirmation == "DELETE":
        deleted = remove_course(course_id)

        if deleted:
            console.print("[green]Course deleted successfully.[/green]")
        else:
            console.print("[yellow]Course ID not found.[/yellow]")
    else:
        console.print("[yellow]Deletion cancelled.[/yellow]")


def course_menu():
    while True:
        console.print("\n[bold cyan]Course Management[/bold cyan]")
        console.print("1. Add course")
        console.print("2. View courses")
        console.print("3. Update course")
        console.print("4. Delete course")
        console.print("5. Back")

        choice = Prompt.ask(
            "Choose an option",
            choices=["1", "2", "3", "4", "5"],
        )

        if choice == "1":
            add_course_menu()
        elif choice == "2":
            show_course_table(list_courses())
        elif choice == "3":
            update_course_menu()
        elif choice == "4":
            delete_course_menu()
        else:
            break


def enroll_student_menu():
    console.print("\n[bold green]Enroll Student in Course[/bold green]")

    student_id = IntPrompt.ask("Student ID")
    course_id = IntPrompt.ask("Course ID")

    success, message = enroll_student(student_id, course_id)

    if success:
        console.print(f"[bold green]{message}[/bold green]")
    else:
        console.print(f"[bold red]{message}[/bold red]")


def drop_enrollment_menu():
    console.print("\n[bold red]Drop Enrollment[/bold red]")

    enrollment_id = IntPrompt.ask("Enrollment ID")
    confirmation = Prompt.ask(
        "Type DROP to confirm",
        choices=["DROP", "CANCEL"],
    )

    if confirmation == "DROP":
        dropped = remove_enrollment(enrollment_id)

        if dropped:
            console.print("[green]Enrollment dropped successfully.[/green]")
        else:
            console.print("[yellow]Enrollment ID not found.[/yellow]")
    else:
        console.print("[yellow]Drop operation cancelled.[/yellow]")


def enrollment_menu():
    while True:
        console.print("\n[bold cyan]Enrollment Management[/bold cyan]")
        console.print("1. Enroll student")
        console.print("2. View enrollments")
        console.print("3. Drop enrollment")
        console.print("4. Back")

        choice = Prompt.ask(
            "Choose an option",
            choices=["1", "2", "3", "4"],
        )

        if choice == "1":
            enroll_student_menu()
        elif choice == "2":
            show_enrollment_table(list_enrollments())
        elif choice == "3":
            drop_enrollment_menu()
        else:
            break


def show_dashboard():
    statistics = get_dashboard()

    table = Table(
        title="CampusFlow Dashboard",
        show_header=False,
    )

    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right", style="green")

    for label, key in [
        ("Total Students", "total_students"),
        ("Total Courses", "total_courses"),
        ("Total Enrollments", "total_enrollments"),
        ("Active Enrollments", "active_enrollments"),
        ("Waitlisted Students", "waitlisted_students"),
        ("Dropped Enrollments", "dropped_enrollments"),
        ("Available Seats", "available_seats"),
    ]:
        table.add_row(label, str(statistics[key]))

    console.print(table)


def export_excel_menu():
    try:
        export_file = export_data_to_excel()

        console.print(
            f"[bold green]Excel report created successfully:[/bold green]\n"
            f"{export_file}"
        )

    except Exception as error:
        console.print(
            f"[bold red]Excel export failed:[/bold red] {error}"
        )


def application_menu():
    while True:
        console.print("\n[bold blue]Main Menu[/bold blue]")
        console.print("1. Student Management")
        console.print("2. Course Management")
        console.print("3. Enrollment Management")
        console.print("4. View Dashboard")
        console.print("5. Export Data to Excel")
        console.print("6. Exit")

        choice = Prompt.ask(
            "Choose an option",
            choices=["1", "2", "3", "4", "5", "6"],
        )

        if choice == "1":
            student_menu()
        elif choice == "2":
            course_menu()
        elif choice == "3":
            enrollment_menu()
        elif choice == "4":
            show_dashboard()
        elif choice == "5":
            export_excel_menu()
        else:
            console.print("[cyan]Thank you for using CampusFlow.[/cyan]")
            break