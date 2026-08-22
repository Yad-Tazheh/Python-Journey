from database.database import SessionLocal
from models.user import User
from utils.password import hash_password


db = SessionLocal()

admin = User(
    username="admin",
    password_hash=hash_password("123456"),
    role="ADMIN",
)

db.add(admin)
db.commit()
db.close()