from db import get_db_connection
from models.goals import GoalRequest, GoalResponse

def fetch_goals(user_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, amount, status FROM goals WHERE id = %s", (user_id,))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return [GoalResponse(**row) for row in result]

def save_goal(user_id: int, data: GoalRequest):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO goals (id, amount, status)
        VALUES (%s, %s, %s)
    """, (user_id, data.amount, data.status))
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Goal added successfully"}
