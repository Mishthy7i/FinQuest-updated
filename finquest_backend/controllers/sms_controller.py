from fastapi import HTTPException
from db import get_db_connection
from utils.llm_utils import query_llm

def parse_and_store_sms(user_id: int, sms_text: str):

    # prompt for the LLM
    system_prompt = (
        "You are a financial assistant. Analyze the following SMS text and extract the following details:\n"
        "- Transaction type (income or expense)\n"
        "- Mode of payment (e.g., card, cash, bank transfer, etc.)\n"
        "- Amount involved\n"
        "Respond in JSON format with keys: 'type', 'mode', 'amount'."
    )

    llm_response = query_llm(system_prompt, sms_text)

    try:
        transaction_details = eval(llm_response)  # Ensure the response is JSON-like
        transaction_type = transaction_details.get("type")
        mode = transaction_details.get("mode")
        amount = transaction_details.get("amount")

        if not transaction_type or not mode or not amount:
            raise HTTPException(status_code=400, detail="Incomplete transaction details from LLM")

        # Insert transaction into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO transactions (user_id, amount, category, mode) VALUES (%s, %s, %s, %s)",
                (user_id, amount, transaction_type, mode)
            )
            conn.commit()
            return {"status": "success", "transaction_details": transaction_details}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process SMS: {str(e)}")