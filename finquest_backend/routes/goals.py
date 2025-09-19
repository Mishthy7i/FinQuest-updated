from fastapi import APIRouter, Depends
from controllers.goals_controller import fetch_goals, save_goal
from models.goals import GoalRequest, GoalResponse
from typing import List
from utils.auth_utils import jwt_bearer

router = APIRouter(prefix="/goals", tags=["Goals"])

@router.get("/", response_model=List[GoalResponse])
def get_goals(user_id: int = Depends(jwt_bearer)):
    return fetch_goals(user_id)

@router.post("/")
def post_goal(data: GoalRequest, user_id: int = Depends(jwt_bearer)):
    return save_goal(user_id, data)
