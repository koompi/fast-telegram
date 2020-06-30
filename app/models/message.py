from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class GetMessage(BaseModel):
    entity: str
    limit: int = 10
    offset_date: Optional[datetime] = None
    max_id: Optional[int] = 0
    min_id: Optional[int] = 0
    search: Optional[str] = None
    from_user: Optional[str] = None
    ids: List[int] = None
    reverse: Optional[bool] = False
