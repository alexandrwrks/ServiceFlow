from fastapi import APIRouter, Depends

from app.modules.order.deps import get_order_service, ExistsOrder
from app.modules.order.schema import OrderParams
from app.modules.order.service import OrderService


router = APIRouter()


@router.post("/")
async def create_orders(
        params: OrderParams,
        service: OrderService = Depends(get_order_service)
):
    return await service.create_order(params)


@router.get("/")
async def get_orders(
        service: OrderService = Depends(get_order_service)
):
    return await service.get_orders()


@router.get("/{order_id}")
async def get_order(
        order: ExistsOrder,
        service: OrderService = Depends(get_order_service)
):
    return await service.get_order_by_id(order)


@router.patch("/{order_id}")
async def update_order(
        order: ExistsOrder,
        params,
        service: OrderService = Depends(get_order_service)
):
    return await service.update_order_info(order.id, params)


@router.post("/{order_id}/confirm")
async def confirm_order(
        order: ExistsOrder,
        service: OrderService = Depends(get_order_service)
):
    return await service.confirm_order(order.id)


@router.post("/{order_id}/assign")
async def assign_order(
        order: ExistsOrder,
        service: OrderService = Depends(get_order_service)
):
    """assign order to employee"""
    return await service.assign_order(order.id)


@router.post("/{order_id}/cancel")
async def cancel_order(
        order: ExistsOrder,
        service: OrderService = Depends(get_order_service)
):
    return await service.cancel_order(order.id)


@router.post("/{order_id}/complete")
async def complete_order(
        order: ExistsOrder,
        service: OrderService = Depends(get_order_service)
):
    return await service.complete_order(order.id)


@router.get("/{order_id}/history")
async def get_history(
        order: ExistsOrder,
        service: OrderService = Depends(get_order_service)
):
    return await service.get_order_history(order.id)