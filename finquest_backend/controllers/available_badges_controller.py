from db import get_db_connection
from models.available_badge import AvailableBadgeRequest, AvailableBadgeResponse

def get_available_badges():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM available_badges")
    badges = cursor.fetchall()
    cursor.close()
    db.close()
    return [AvailableBadgeResponse(**row) for row in badges]

def create_available_badge(data: AvailableBadgeRequest):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO available_badges (badge_image, badge_desc, badge_url, badge_criteria)
        VALUES (%s, %s, %s, %s)
    """, (
        data.badge_image,
        data.badge_desc,
        data.badge_url,
        data.badge_criteria
    ))
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Badge successfully added"}
