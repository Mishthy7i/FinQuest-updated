from db import get_db_connection
from fastapi import HTTPException
from models.profile_build import ProfileBuildRequest, ProfileBuildResponse

def fetch_profile_build(user_id: int) -> ProfileBuildResponse:
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM profile_build WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()

    if result:
        return ProfileBuildResponse(**result)
    else:
        raise HTTPException(status_code=404, detail="Profile build not found")

def save_profile_build(user_id: int, data: ProfileBuildRequest):
    db = get_db_connection()
    cursor = db.cursor()

    # Check if entry exists
    cursor.execute("SELECT id FROM profile_build WHERE id = %s", (user_id,))
    existing = cursor.fetchone()

    if existing:
        # Update existing
        cursor.execute("""
            UPDATE profile_build SET
                Food = %s, Travel = %s, Shopping = %s, Grocery = %s,
                Personal = %s, Education = %s, Bills = %s, Other = %s
            WHERE id = %s
        """, (
            data.Food, data.Travel, data.Shopping, data.Grocery,
            data.Personal, data.Education, data.Bills, data.Other, user_id
        ))
    else:
        # Insert new
        cursor.execute("""
            INSERT INTO profile_build (
                id, Food, Travel, Shopping, Grocery,
                Personal, Education, Bills, Other
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, data.Food, data.Travel, data.Shopping, data.Grocery,
            data.Personal, data.Education, data.Bills, data.Other
        ))

    db.commit()
    cursor.close()
    db.close()

    return {"message": "Profile build saved successfully"}
