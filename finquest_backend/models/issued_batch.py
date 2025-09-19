from pydantic import BaseModel
from datetime import datetime

class IssuedBatchResponse(BaseModel):
    badge_id: int
    id: int
    issued_at: datetime
