from db import get_db_connection
from models.streaks import StreakResponse
from fastapi import HTTPException

def get_streak(user_id: int) -> StreakResponse:
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM streaks WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    db.close()
    if row:
        return StreakResponse(**row)
    else:
        raise HTTPException(status_code=404, detail="Streak not found")

def get_all_streaks():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        # Get all streaks with user information
        cursor.execute("""
            SELECT 
                s.id,
                s.count,
                u.name,
                u.username
            FROM streaks s
            LEFT JOIN users u ON s.id = u.id
            ORDER BY s.count DESC
        """)
        streaks = cursor.fetchall()
        
        return [
            {
                "id": streak["id"],
                "count": streak["count"],
                "name": streak["name"] or streak["username"] or f"User {streak['id']}",
                "username": streak["username"]
            }
            for streak in streaks
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        db.close()
