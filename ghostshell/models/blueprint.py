
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class Blueprint(BaseModel):
    
    # === Core Persona & Context ===
    voice: str = ""
    core_philosophy: str = ""
    target_audience: str = ""
    niche: str = ""

    # === Topic Flavour & Positioning ===
    intellectual_positioning: str = ""
    topic_flavour: str = ""
    linguistic_markers: str = ""
    
    # === Style & Structure ===
    stylistic_fingerprint: str = ""
    opening_hook_psychology: str = ""
    narrative_architecture: str = ""
    pacing_and_density: str = ""

    # === Constraints & Anti-Patterns ===
    anti_patterns: str = ""

    # === Metadata ===
    existing_topics: List[str] = Field(default_factory=list)
    last_distilled: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
