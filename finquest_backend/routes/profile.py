from fastapi import APIRouter, Depends
from controllers.profile_controller import fetch_user_profile
from models.profile import ProfileResponse
from utils.auth_utils import jwt_bearer

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=ProfileResponse)
def get_profile(user_id: int = Depends(jwt_bearer)):
    return fetch_user_profile(user_id)