from app.utils import hash_password
from app.database import SessionLocal
from app import models

db = SessionLocal()

# Rehash all admin passwords if not already hashed
admins = db.query(models.Admin).all()
for admin in admins:
    if not admin.password.startswith("$2b$"):  # bcrypt hashes start with $2b$
        admin.password = hash_password(admin.password)

db.commit()
