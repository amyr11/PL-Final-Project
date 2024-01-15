from supabase import create_client, Client
from common.types import *

class Database:
    def __init__(self, url: str, key: str) -> None:
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
        return self.client.table('student_info').select('*').eq('student_id', student_id).execute().data[0]
    
    def delete_student(self, student_id: str) -> None:
        """Delete a student's data from the database.
        
        Args:
            student_id (str): The student's ID.

        Returns:
            None
        """
        self.client.table('student_info').delete().eq('student_id', student_id).execute()

    def update_student(self, student_id: str, data: Student) -> Student:
        """Update a student's data in the database.
        
        Args:
            student_id (str): The student's ID.
            data (Student): The student's data to update.

        Returns:
            Student: The student's updated data.
        """
        self.client.table('student_info').update(data).eq('student_id', student_id).execute()

    def insert_student(self, data: Student) -> Student:
        """Insert a student's data into the database.

        Args:
            data (Student): The student's data to insert.

        Returns:
            Student: The student's inserted data.
        """
        self.client.table('student_info').insert(data).execute()

    def get_grade(self, grade_id: int):
        """Get a grade's data from the database.

        Args:
            grade (str): The grade's ID.

        Returns:
            Grade: The grade's data.
        """
        return self.client.table('grades').select('*').eq('grade', grade_id).execute().data[0]
    
    def delete_grade(self, grade_id: int) -> None:
        """Delete a grade's data from the database.
        
        Args:
            grade (int): The grade's ID.

        Returns:
            None
        """
        self.client.table('grades').delete().eq('grade', grade_id).execute()

    def update_grade(self, grade_id: int, data: Grade) -> Grade:
        """Update a grade's data in the database.
        
        Args:
            grade (int): The grade's ID.
            data (Grade): The grade's data to update.

        Returns:
            Grade: The grade's updated data.
        """
        self.client.table('grades').update(data).eq('grade', grade_id).execute()

    def insert_grade(self, data: Grade) -> Grade:
        """Insert a grade's data into the database.

        Args:
            data (Grade): The grade's data to insert.

        Returns:
            Grade: The grade's inserted data.
        """
        self.client.table('grades').insert(data).execute()

    def get_client(self) -> Client:
        return self.client