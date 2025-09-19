from fastapi import APIRouter, Depends
from controllers.streaks_controller import get_streak
from models.streaks import StreakResponse
from utils.auth_utils import jwt_bearer

router = APIRouter(prefix="/streaks", tags=["Streaks"])

@router.get("/", response_model=StreakResponse)
def fetch_streak(user_id: int = Depends(jwt_bearer)):
    return get_streak(user_id)
