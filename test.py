from httpx import get
from utils.database import Database

db = Database()

db.delete_grade(0)
