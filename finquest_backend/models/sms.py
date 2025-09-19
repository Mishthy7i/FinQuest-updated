from pydantic import BaseModel

class ParseSMSRequest(BaseModel):
    sms: str

class ParseSMSResponse(BaseModel):
    status: str
    transaction_details: dict | None = None