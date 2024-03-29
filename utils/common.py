from typing import TypedDict


class Student(TypedDict):
    """Student data type.

    Attributes:
        student_id (str): The student's ID.
        first_name (str): The student's first name.
        middle_name (str): The student's middle name.
        last_name (str): The student's last name.
        course_id (int): The student's course.
        year_level (int): The student's year level.
        email (str): The student's email.
        contact_number (str): The student's contact number.
    """

    student_id: str
    first_name: str
    middle_name: str
    last_name: str
    course_id: int
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
        subject_code (str): The subject's code.
        messaged (bool): Whether the student has been messaged.
        created_at (int): The time the grade was created.
        updated_at (int): The time the grade was updated.
    """

    grade_id: int
    student_id: str
    grade: float | None
    remark_id: int
    year: int
    sem: int
    subject_code: str
    messaged: bool
    created_at: str
    updated_at: str


class LoginInfo(TypedDict):
    """Login info data type.

    Attributes:
        username (str): The username.
        employee_number (int): The employee number.
        hash (str): The password hash.
        first_name (str): The first name.
        middle_name (str): The middle name.
        last_name (str): The last name.
    """

    employee_number: str
    hash: str
    first_name: str
    middle_name: str
    last_name: str


class StudentRequest(TypedDict):
    id: int
    student_id: str
    mode: str
    document_type_id: int
    request_amount: int
    purpose: str
    total: float
    receipt_number: str
    request_date: int
    receive_date: int
    student_request_status_id: int
    created_at: str
    updated_at: str
    messaged: bool


valid_tables = [
    "document_type",
    "grades",
    "login",
    "remarks",
    "request_statuses",
    "student_info",
    "student_requests",
    "subjects",
    "courses",
]

remarks = {"incomplete_grade": 3, "failed_grade": 2, "passed_grade": 1}

message_templates = {
    "incomplete_grade": "Hi {first_name} {last_name}, you have an incomplete grade in: {subjects}. Please contact your professor for more information.",
    "failed_grade": "Hi {first_name} {last_name}, you have a failed grade in: {subjects}. Please contact your professor for more information.",
    "requested_document": "Hi {first_name} {last_name}, your {document} is now ready for pickup. Please proceed to the registrar's office.",
}
