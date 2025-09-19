from fastapi import HTTPException
from db import get_db_connection
from models.transaction import AddTransactionRequest
from datetime import datetime

def add_transaction(user_id: int, transaction: AddTransactionRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO transactions (user_id, amount,category,type, mode, created_at) VALUES (%s, %s,%s, %s, %s, %s)",
            (user_id, transaction.amount, transaction.category, transaction.type,transaction.mode, datetime.now())
        )
        conn.commit()
        
        # transaction ID
        transaction_id = cursor.lastrowid
        
        return {
            "message": "Transaction added successfully",
            "transaction_id": transaction_id
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def get_user_transactions(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Fix: Add comma after user_id to make it a proper tuple
        cursor.execute(
            "SELECT id, user_id, amount, category,type, mode, created_at FROM transactions WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)  # Note the comma after user_id
        )
        transactions = cursor.fetchall()
        
        result = []
        for transaction in transactions:
            result.append({
                "id": transaction[0],
                "user_id": transaction[1],
                "amount": transaction[2],
                "category": transaction[3],
                "type":transaction[4],
                "mode": transaction[5],
                "created_at": transaction[6]
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()