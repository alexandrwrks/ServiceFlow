from pydantic import BaseModel, Field
from pydantic.v1 import EmailStr

from database.models import OrderStatusType


class OrderParams(BaseModel):
    service_id: int = Field(gt=0)
    first_name: str
    last_name: str
    phone: str
    notes: str | None = Field(default=None, max_length=500)


