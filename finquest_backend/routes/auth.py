from fastapi import APIRouter, Depends 
from models.auth import SignupRequest, SignupResponse, LoginRequest, LoginResponse
from controllers.auth_controller import create_user, login_user
from utils.auth_utils import jwt_bearer # verify_token to test each request with jet token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=SignupResponse)
def create_user_route(user: SignupRequest):
    return create_user(user)

@router.post("/login", response_model=LoginResponse)
def login_user_route(user: LoginRequest):
    return login_user(user)

# a test route to test jwt tokens working
@router.get("/testjwt")
def test_jwt_route(user_id: int = Depends(jwt_bearer)): # Depends to use verify_token function on request before accessing controller
    return {
        "message": "JWT token is valid",
        "user_id": user_id,
        "status": "authenticated"
    }