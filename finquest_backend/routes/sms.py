from fastapi import APIRouter, Depends
from models.sms import ParseSMSRequest, ParseSMSResponse
from controllers.sms_controller import parse_and_store_sms
from utils.auth_utils import jwt_bearer

router = APIRouter(prefix="/sms", tags=["SMS"])

@router.post("/parse", response_model=ParseSMSResponse)
async def parse_sms(payload: ParseSMSRequest, user_id: int = Depends(jwt_bearer)):
    return parse_and_store_sms(user_id, payload.sms)