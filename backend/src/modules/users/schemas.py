from datetime import datetime

from pydantic import BaseModel, ConfigDict
import uuid

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    email: str | None
    created_at: datetime
    external_id: str
    avatar: str
    
class DiscordUserSchema(BaseModel):
    id: str
    username: str
    email: str | None = None
    avatar: str | None = None