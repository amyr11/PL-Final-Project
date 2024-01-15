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

class Grade(TypedDict):
    """Grade data type.

    Attributes:
        grade_id (int): The grade's ID.
        student_id (str): The student's ID.
        grade (float): The grade.
        remark_id (int): The remark's ID.
        year (int): The school year.
        sem (int): The semester.
        subject_id (int): The subject's ID.
        messaged (bool): Whether the student has been messaged.
    """
    grade_id: int
    student_id: str
    grade: float
    remark_id: int
    year: int
    sem: int
    subject_id: int
    messaged: bool

