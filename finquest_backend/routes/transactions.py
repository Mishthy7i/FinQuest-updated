from fastapi import APIRouter, Depends, Query
from typing import List
from models.transaction import (
    AddTransactionRequest, 
    TransactionResponse, 
    AddTransactionResponse
)
from controllers.transaction_controller import (
    add_transaction,
    get_user_transactions,
)
from utils.auth_utils import jwt_bearer

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/add", response_model=AddTransactionResponse)
def add_transaction_route(
    transaction: AddTransactionRequest,
    user_id: int = Depends(jwt_bearer)
):
    return add_transaction(user_id, transaction)

@router.get("/", response_model=List[TransactionResponse])
def get_transactions_route(
    user_id: int = Depends(jwt_bearer),
):
    return get_user_transactions(user_id)