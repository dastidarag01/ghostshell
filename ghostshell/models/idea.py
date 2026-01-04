
from datetime import datetime
from pydantic import BaseModel, Field
import uuid as uuid_lib


class SuggestedIdea(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid_lib.uuid4()))
    topic: str
    angle: str
    hook_summary: str
    suggested_at: datetime = Field(default_factory=datetime.now)
