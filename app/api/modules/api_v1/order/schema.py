from pydantic import BaseModel

from app.database.models import OrderStatusType


class OrderParams(BaseModel):
    name: str
    phone: str
    position: OrderStatusType