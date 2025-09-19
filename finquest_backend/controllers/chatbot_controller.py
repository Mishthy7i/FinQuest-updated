import os
from openai import OpenAI
from fastapi import HTTPException
from db import get_db_connection

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_user_profile(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, dob, salary FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        cursor.close()
        conn.close()

def get_user_transactions_summary(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get transaction types and categories summary
        cursor.execute("""
            SELECT 
                type,
                category,
                COUNT(*) as count,
                SUM(amount) as total_amount,
                AVG(amount) as avg_amount
            FROM transactions 
            WHERE user_id = %s 
            GROUP BY type, category
            ORDER BY type, total_amount DESC
        """, (user_id,))
        transaction_summary = cursor.fetchall()
        
        # Get recent transactions for context
        cursor.execute("""
            SELECT type, category, amount, mode, created_at
            FROM transactions 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 10
        """, (user_id,))
        recent_transactions = cursor.fetchall()
        
        return {
            "summary": transaction_summary,
            "recent": recent_transactions
        }
    finally:
        cursor.close()
        conn.close()

def ask_chatbot(user_id: int, question: str):
    try:
        user = get_user_profile(user_id)
        transactions_data = get_user_transactions_summary(user_id)

        # Build transaction context for the prompt
        transaction_context = ""
        if transactions_data["summary"]:
            transaction_context += "\n\nUser's Transaction Summary:\n"
            for trans in transactions_data["summary"]:
                transaction_context += f"- {trans['type'].title()} in {trans['category']}: {trans['count']} transactions, Total: ₹{trans['total_amount']:.2f}, Average: ₹{trans['avg_amount']:.2f}\n"
        
        if transactions_data["recent"]:
            transaction_context += "\nRecent Transactions:\n"
            for trans in transactions_data["recent"]:
                transaction_context += f"- {trans['created_at'].strftime('%Y-%m-%d')}: {trans['type'].title()} of ₹{trans['amount']:.2f} in {trans['category']} via {trans['mode']}\n"

        # Custom system prompt
        system_prompt = (
            f"You are a helpful personal finance assistant for a user named {user['name']}, "
            f"who was born in {user['dob']} and earns ₹{user['salary']} per month. "
            f"Provide personalized answers and financial tips based on their profile and transaction history."
            f"{transaction_context}"
            f"\n\nUse this information to provide contextual and personalized financial advice."
        )

        completion = client.chat.completions.create(
            model="gpt-4o",  # or gpt-4.1 / gpt-4o-mini for cheaper responses
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )

        return {"answer": completion.choices[0].message.content.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
