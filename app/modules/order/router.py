from fastapi import APIRouter, Depends

from app.modules.order.deps import get_order_service
from app.modules.order.schema import OrderParams
from app.modules.order.service import OrderService


router = APIRouter()


@router.post("/")
async def create_orders(
    params: OrderParams, service: OrderService = Depends(get_order_service)
):
    return await service.create_order(params)


@router.get("/")
async def get_orders():
    return


@router.get("/{order_id}")
async def get_order(order_id: int):
    return


@router.patch("/{order_id}")
async def update_order(order_id: int):
    return


@router.post("/{order_id}/assign")
async def assign_order(order_id: int):
    """assign order to employee"""
    return


@router.post("/{order_id}/schedule")
async def schedule_order(order_id: int):
    """schedule order to employee"""
    return


@router.post("/{order_id}/cancel")
async def cancel_order(order_id: int):
    return
