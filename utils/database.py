from supabase import create_client, Client
from .tables import *
from datetime import datetime
import os
import hashlib

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_API_KEY")


class Database:
    def __init__(self, url: str = url, key: str = key) -> None:
        self.url = url
        self.key = key
        self.client: Client = create_client(url, key)

    def get_student(self, student_id: str) -> Student:
        """Get a student's data from the database.

        Args:
            student_id (str): The student's ID.

        Returns:
            Student: The student's data.
        """
        student = (
            self.client.table("student_info")
            .select("*")
            .eq("student_id", student_id)
            .execute()
            .data
        )
        
        if student:
            return student[0]
        else:
            return None
    
    def get_student_grade(self, student_id: str, year: int, sem: int) -> Student:
        """Get a student's data from the database.

        Args:
            student_id (str): The student's ID.

        Returns:
            Student: The student's data.
        """
        student = (
            self.client.table("grades")
            .select("remarks(remark), subjects(*), *")
            .eq("student_id", student_id)
            .eq("year", year)
            .eq("sem", sem)
            .execute()
            .data
        )
        
        if student:
            return student
        else:
            return None

    def delete_student(self, student_id: str) -> None:
        """Delete a student's data from the database.

        Args:
            student_id (str): The student's ID.

        Returns:
            None
        """
        self.client.table("student_info").delete().eq(
            "student_id", student_id
        ).execute()

    def update_student(self, student_id: str, data: Student) -> Student:
        """Update a student's data in the database.

        Args:
            student_id (str): The student's ID.
            data (Student): The student's data to update.

        Returns:
            Student: The student's updated data.
        """
        self.client.table("student_info").update(data).eq(
            "student_id", student_id
        ).execute()

    def insert_student(self, data: Student) -> Student:
        """Insert a student's data into the database.

        Args:
            data (Student): The student's data to insert.

        Returns:
            Student: The student's inserted data.
        """
        self.client.table("student_info").insert(data).execute()

    def get_all_grade(self, remark=None):
        """Get all grades info from the database.

        Args:
            status (int) (optional): The remark's ID. 1 for passed, 2 for failed, 3 for incomplete.

        Returns:
            Grades: The grades' data.
        """

        select_stmt = "student_id, student_info(last_name, first_name, middle_name, contact_number), remarks(remark), subjects(title), year, sem"

        if remark:
            return (
                self.client.table("grades")
                .select(select_stmt)
                .eq("remark_id", remarks[remark])
                .execute()
                .data
            )
        else:
            return self.client.table("grades").select(select_stmt).execute().data

    def delete_grade(self, grade_id: int) -> None:
        """Delete a grade's data from the database.

        Args:
            grade (int): The grade's ID.

        Returns:
            None
        """
        self.client.table("grades").delete().eq("grade_id", grade_id).execute()

    def update_grade(self, grade_id: int, data: Grade) -> Grade:
        now = datetime.now().timestamp()
        """Update a grade's data in the database.
        
        Args:
            grade (int): The grade's ID.
            data (Grade): The grade's data to update.

        Returns:
            Grade: The grade's updated data.
        """
        data["updated_at"] = str(datetime.fromtimestamp(now))
        self.client.table("grades").update(data).eq("grade_id", grade_id).execute()

    def insert_grade(self, data: Grade) -> Grade:
        """Insert a grade's data into the database.

        Args:
            data (Grade): The grade's data to insert.

        Returns:
            Grade: The grade's inserted data.
        """
        self.client.table("grades").insert(data).execute()

    def get_login_info(self, employee_number: str) -> LoginInfo:
        """Get a login's data from the database.

        Args:
            employee_number (str): The login's employee_number.

        Returns:
            LoginInfo: The login's data.
        """
        return (
            self.client.table("login")
            .select("*")
            .eq("employee_number", employee_number)
            .execute()
            .data[0]
        )

    def delete_login_info(self, employee_number: str) -> None:
        """Delete a login's data from the database.

        Args:
            employee_number (str): The login's employee_number.

        Returns:
            None
        """
        self.client.table("login").delete().eq(
            "employee_number", employee_number
        ).execute()

    def update_login_info(self, employee_number: str, data: LoginInfo) -> LoginInfo:
        """Update a login's data in the database.

        Args:
            employee_number (str): The login's employee_number.
            data (LoginInfo): The login's data to update.

        Returns:
            LoginInfo: The login's updated data.
        """
        self.client.table("login").update(data).eq(
            "employee_number", employee_number
        ).execute()

    def insert_login_info(self, data: LoginInfo) -> LoginInfo:
        """Insert a login's data into the database.

        Args:
            data (LoginInfo): The login's data to insert.

        Returns:
            LoginInfo: The login's inserted data.
        """
        self.client.table("login").insert(data).execute()

    def get_student_request(self, id: int) -> StudentRequest:
        """Get a student request's data from the database.

        Args:
            id (int): The student request's ID.

        Returns:
            StudentRequest: The student request's data.
        """
        return (
            self.client.table("student_requests")
            .select("*")
            .eq("id", id)
            .execute()
            .data[0]
        )

    def get_all_ready_requests(self):
        """Get all document requests info that are ready to claim from the database.

        Returns:
            Document requests: The requests' data.
        """

        select_stmt = "student_id, student_info(last_name, first_name, middle_name, contact_number), document_type(type), *"

        return (
            self.client.table("student_requests")
            .select(select_stmt)
            .eq("student_request_status_id", 2)
            .execute()
            .data
        )

    def delete_student_request(self, id: int) -> None:
        """Delete a student request's data from the database.

        Args:
            id (int): The student request's ID.

        Returns:
            None
        """
        self.client.table("student_requests").delete().eq("id", id).execute()

    def update_student_request(self, id: int, data: StudentRequest) -> StudentRequest:
        now = datetime.now().timestamp()
        """Update a student request's data in the database.
        
        Args:
            id (int): The student request's ID.
            data (StudentRequest): The student request's data to update.

        Returns:
            StudentRequest: The student request's updated data.
        """
        data["updated_at"] = str(datetime.fromtimestamp(now))
        self.client.table("student_requests").update(data).eq("id", id).execute()

    def insert_student_request(self, data: StudentRequest) -> StudentRequest:
        """Insert a student request's data into the database.

        Args:
            data (StudentRequest): The student request's data to insert.

        Returns:
            StudentRequest: The student request's inserted data.
        """
        self.client.table("student_requests").insert(data).execute()

    def get_all(self, table: str) -> list:
        """Get all data from a table.

        Args:
            table (str): The table to get data from.

        Returns:
            list: A list of data from the table.
        """
        if table not in valid_tables:
            raise Exception(f"Invalid table: {table}. Valid tables are: {valid_tables}")
        return self.client.table(table).select("*").execute().data

    def verify_login(self, employee_number: str, password: str) -> bool:
        """Verify the login credentials against the database.

        Args:
            employee_number (str): The employee number.
            password (str): The password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """

        md5_password = hashlib.md5(password.encode()).hexdigest()

        return (
            self.client.table("login")
            .select("*")
            .eq("employee_number", employee_number)
            .eq("hash", md5_password)
            .execute()
            .data
        )

    def get_client(self) -> Client:
        return self.client
