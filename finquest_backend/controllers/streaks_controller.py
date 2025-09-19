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
