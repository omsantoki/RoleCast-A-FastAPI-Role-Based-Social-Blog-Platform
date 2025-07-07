# RoleCast – A FastAPI Role-Based Social Blog Platform

RoleCast is a modern social blogging platform built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, with a robust role-based access system. Users can create, manage, and schedule posts, while admins can manage user content at a broader level.

---

## 🚀 Features

- 🔐 **JWT-based Authentication (OAuth2)**
- 👤 **Role-based Access Control (User/Admin)**
- 📝 **Users can create, update, delete, and schedule posts**
- 📅 **Post scheduling using APScheduler**
- 🗳️ **Post voting system**
- 📊 **Admins can view and manage all users’ posts**
- 📦 **Alembic for migrations**
- 🛡️ **Password hashing and secure login system**

---

## 📁 Project Structure

```bash
RoleCast/
│
├── hashed_password.py           # Password hashing and verification (moved from app/)
│
├── app/
│   ├── main.py                  # App entry point
│   ├── config.py                # App settings and environment config
│   ├── database.py              # DB connection logic
│   ├── models.py                # SQLAlchemy models
│   ├── schemas.py               # Pydantic schemas
│   ├── oauth2.py                # Token handling & authentication
│   ├── routers/
│   │   ├── user.py              # User-related routes
│   │   ├── auth.py              # Login & auth routes
│   │   ├── post.py              # Post management routes
│   │   ├── admin.py             # Admin-only routes
│   └── __pycache__/             # Ignored Python cache files
│
├── alembic/                     # Alembic migration files
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── venv/                        # Virtual environment (should be ignored)
├── .env                         # Environment variables (should be ignored)
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
└── README.md                    
