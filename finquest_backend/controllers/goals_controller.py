from db import get_db_connection
from models.goals import GoalRequest, GoalResponse
from fastapi import HTTPException

def fetch_goals(user_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    # Since goals table doesn't have user_id, we'll get all goals for now
    # You might want to add user_id to the goals table schema
    cursor.execute("SELECT id, amount, status FROM goals")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return [GoalResponse(**row) for row in result]

def save_goal(user_id: int, data: GoalRequest):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO goals (amount, status)
        VALUES (%s, %s)
    """, (data.amount, data.status))
    db.commit()
    goal_id = cursor.lastrowid
    cursor.close()
    db.close()
    return {"message": "Goal added successfully", "goal_id": goal_id}

def update_goal(goal_id: int, user_id: int, data: GoalRequest):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE goals 
        SET amount = %s, status = %s
        WHERE id = %s
    """, (data.amount, data.status, goal_id))
    db.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    db.close()
    
    if affected_rows > 0:
        return {"message": "Goal updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Goal not found")
