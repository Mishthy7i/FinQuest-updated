from pydantic import BaseModel
from typing import Optional

class ProfileBuildRequest(BaseModel):
    Food: Optional[float] = 0
    Travel: Optional[float] = 0
    Shopping: Optional[float] = 0
    Grocery: Optional[float] = 0
    Personal: Optional[float] = 0
    Education: Optional[float] = 0
    Bills: Optional[float] = 0
    Other: Optional[float] = 0

class ProfileBuildResponse(ProfileBuildRequest):
    id: int
