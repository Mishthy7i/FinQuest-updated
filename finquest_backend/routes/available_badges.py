from fastapi import APIRouter, Depends
from typing import List
from utils.auth_utils import jwt_bearer
from controllers.available_badges_controller import (
    get_available_badges,
    create_available_badge
)
from models.available_badge import AvailableBadgeRequest, AvailableBadgeResponse

router = APIRouter(prefix="/available_badges", tags=["Available Badges"])

@router.get("/", response_model=List[AvailableBadgeResponse])
def available_badges_get(user_id: int = Depends(jwt_bearer)):
    return get_available_badges()

@router.post("/")
def available_badges_post(data: AvailableBadgeRequest, user_id: int = Depends(jwt_bearer)):
    return create_available_badge(data)
