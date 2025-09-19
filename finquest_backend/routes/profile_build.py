from fastapi import APIRouter, Depends, HTTPException
from controllers.profile_build_controller import fetch_profile_build, save_profile_build
from models.profile_build import ProfileBuildResponse, ProfileBuildRequest
from utils.auth_utils import jwt_bearer

router = APIRouter(prefix="/profile_build", tags=["Profile Build"])

@router.get("/", response_model=ProfileBuildResponse)
def get_profile_build(user_id: int = Depends(jwt_bearer)):
    return fetch_profile_build(user_id)

@router.post("/create")
def post_profile_build(data: ProfileBuildRequest, user_id: int = Depends(jwt_bearer)):
    return save_profile_build(user_id, data)
