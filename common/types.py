from typing import TypedDict

class Student(TypedDict):
    student_id: str
    first_name: str
    middle_name: str
    last_name: str
    course: str
    year_level: int
    email: str
    contact_number: str