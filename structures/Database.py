from supabase import create_client, Client

class Database:
    def __init__(self, url: str, key: str) -> None:
        self.url = url
        self.key = key
        self.client: Client = create_client(url, key)

    def get_student(self, student_id: str) -> dict:
        return self.client.table('student_info').select('*').eq('student_id', student_id).execute().data[0]
    
    def delete_student(self, student_id: str) -> None:
        self.client.table('student_info').delete().eq('student_id', student_id).execute()

    def update_student(self, student_id: str, data: dict) -> None:
        self.client.table('student_info').update(data).eq('student_id', student_id).execute()

    def insert_student(self, data: dict) -> None:
        self.client.table('student_info').insert(data).execute()

    def get_client(self) -> Client:
        return self.client