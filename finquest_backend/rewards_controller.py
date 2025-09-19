from db import get_db_connection

def update_user_rewards(user_id: int, amount: float):
    db = get_db_connection()
    cursor = db.cursor()

    xp_earned = int(amount // 100) * 10
    cursor.execute("SELECT xp FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    current_xp = result[0] if result and result[0] else 0
    new_xp = current_xp + xp_earned

    cursor.execute("UPDATE users SET xp = %s WHERE id = %s", (new_xp, user_id))
    db.commit()

    badge = None
    if new_xp >= 500:
        badge = "Master Saver"
    elif new_xp >= 200:
        badge = "Budget Ninja"
    elif new_xp >= 100:
        badge = "Smart Spender"

    if badge:
        cursor.execute("SELECT badges FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        existing_badges = result[0] or ""
        badge_list = existing_badges.split(",") if existing_badges else []
        if badge not in badge_list:
            badge_list.append(badge)
        updated_badges = ",".join(badge_list)
        cursor.execute("UPDATE users SET badges = %s WHERE id = %s", (updated_badges, user_id))
        db.commit()

    cursor.close()
    db.close()
