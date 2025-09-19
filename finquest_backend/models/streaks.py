from pydantic import BaseModel

class StreakResponse(BaseModel):
    id: int
    count: int
