from pydantic import BaseModel

class AvailableBadgeRequest(BaseModel):
    badge_image: str
    badge_desc: str
    badge_url: str
    badge_criteria: str

class AvailableBadgeResponse(AvailableBadgeRequest):
    badge_id: int
