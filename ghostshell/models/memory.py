
from pydantic import BaseModel


class Memory(BaseModel):
    topic: str = ""
    content: str = ""
