from fastapi import APIRouter, Depends
from controllers.issued_batches_controller import fetch_issued_batches
from models.issued_batch import IssuedBatchResponse
from typing import List
from utils.auth_utils import jwt_bearer

router = APIRouter(prefix="/issued_batches", tags=["Issued Badges"])

@router.get("/", response_model=List[IssuedBatchResponse])
def get_issued_batches(user_id: int = Depends(jwt_bearer)):
    return fetch_issued_batches(user_id)
