from pydantic import BaseModel
from datetime import date

class ProfileResponse(BaseModel):
    user_id: int
    name: str
    email: str
    dob: date
    salary: float