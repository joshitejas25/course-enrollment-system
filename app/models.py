from dataclasses import dataclass


@dataclass
class Student:
    name: str
    email: str
    phone: str
    department: str
    year: int
    id: int | None = None


@dataclass
class Course:
    course_code: str
    course_name: str
    instructor: str
    credits: int
    capacity: int
    prerequisite: str = ""
    id: int | None = None