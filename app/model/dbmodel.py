from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Schema


class DateTimeModelMixin(BaseModel):
    created_at = Schema(..., alias='createdAt')
    created_at: Optional[datetime]
    updated_at = Schema(..., alias='updatedAt')
    updated_at: Optional[datetime]
