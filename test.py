from utils.database import Database

db = Database()
documents = db.get_document_requests_by_status("pending")

print(documents)