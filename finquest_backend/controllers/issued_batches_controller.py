from db import get_db_connection
from models.issued_batch import IssuedBatchResponse

def fetch_issued_batches(user_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT badge_id, id, issued_at FROM issued_badges WHERE id = %s
    """, (user_id,))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return [IssuedBatchResponse(**row) for row in result]
