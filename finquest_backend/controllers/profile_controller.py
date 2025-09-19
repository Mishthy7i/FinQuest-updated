from fastapi import HTTPException
from db import get_db_connection

def fetch_user_profile(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name, email, dob, salary FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "user_id": user_id,
            "name": user[0],
            "email": user[1],
            "dob": user[2], 
            "salary": float(user[3])
        }
    finally:
        cursor.close()
        conn.close()