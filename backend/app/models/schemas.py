from pydantic import BaseModel
from typing import List, Optional

# ============================================
# USER PROFILE SCHEMAS
# ============================================

class BasicProfileCreate(BaseModel):
    full_name: str  # Required now
    username: str   # Required now
    organization: Optional[str] = None
    field_of_study: Optional[str] = None
    phone: Optional[str] = None
    profile_pic: Optional[str] = None