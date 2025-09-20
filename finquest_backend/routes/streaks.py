from fastapi import APIRouter, Depends
from controllers.streaks_controller import get_streak, get_all_streaks
from models.streaks import StreakResponse
from utils.auth_utils import jwt_bearer

router = APIRouter(prefix="/streaks", tags=["Streaks"])

@router.get("/", response_model=StreakResponse)
def fetch_streak(user_id: int = Depends(jwt_bearer)):
    return get_streak(user_id)

@router.get("/all")
def fetch_all_streaks(user_id: int = Depends(jwt_bearer)):
    return get_all_streaks()
