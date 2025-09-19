from models.auth import SignupRequest, LoginRequest
from fastapi import HTTPException
from db import get_db_connection
import hashlib
from utils.auth_utils import create_token

def create_user(data: SignupRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (data.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")

        password_hash = hashlib.sha256(data.password.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, name, email, password, dob, salary) VALUES (%s, %s, %s, %s, %s, %s)",
            (data.username, data.name, data.email, password_hash, data.dob, data.salary)
        )
        conn.commit()
        return {"message": "Signup successful", "username": data.username}
    finally:
        cursor.close()
        conn.close()

def login_user(data: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        password_hash = hashlib.sha256(data.password.encode()).hexdigest()
        cursor.execute("SELECT id, username FROM users WHERE email=%s AND password=%s", (data.email, password_hash))
        user = cursor.fetchone()

        if user:
            token = create_token(user[0])
            return {"message": "Login successful", "username": user[1], "token": token}

        raise HTTPException(status_code=401, detail="Invalid credentials")
    finally:
        cursor.close()
        conn.close()
