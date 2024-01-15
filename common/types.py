from typing import TypedDict

class Student(TypedDict):
    """Student data type.

    Attributes:
        student_id (str): The student's ID.
        first_name (str): The student's first name.
        middle_name (str): The student's middle name.
        last_name (str): The student's last name.
        course (str): The student's course.
        year_level (int): The student's year level.
        email (str): The student's email.
        contact_number (str): The student's contact number.
    """
    student_id: str
    first_name: str
    middle_name: str
    last_name: str
    course: str
    year_level: int
    email: str
    contact_number: str