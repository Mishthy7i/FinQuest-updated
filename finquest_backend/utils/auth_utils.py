import jwt
import os
from datetime import datetime, timedelta
from fastapi import Request, HTTPException # because jwt is send in request header not body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

JWT_SECRET = os.getenv("JWT_SECRET") or "mysecretjwttoken" # default secret if env not worked

# generate token for user
def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(days=7) # Token valid for 7 days
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# code from fastapi docs
def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return self.get_user_id_from_token(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decode_jwt(jwtoken)
            return True if payload else False
        except:
            return False

    def get_user_id_from_token(self, jwtoken: str) -> int:
        payload = decode_jwt(jwtoken)
        return payload["user_id"]

# Create an instance of JWTBearer for use in routes
jwt_bearer = JWTBearer()