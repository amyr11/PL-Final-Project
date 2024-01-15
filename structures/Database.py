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

    def get_client(self) -> Client:
        return self.client