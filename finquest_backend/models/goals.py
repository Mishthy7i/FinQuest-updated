from pydantic import BaseModel
from typing import Literal

class GoalRequest(BaseModel):
    amount: float
    status: Literal["completed", "incompleted", "deleted"]

class GoalResponse(GoalRequest):
    id: int
