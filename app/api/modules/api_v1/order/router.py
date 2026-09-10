from fastapi import APIRouter, Depends


router = APIRouter()


@router.post("/orders")
async def create_orders(
        params: OrderParams,
        service: OrderService = Depends(get_order_service)
):
    return await service.create_orders(params)


@router.get("/orders")
async def get_orders():
    return


@router.get("/orders/{order_id}")
async def get_order(order_id: int):
    return


@router.patch("/orders/{order_id}")
async def update_order(order_id: int):
    return


@router.post("/orders/{order_id}/assign")
async def assign_order(order_id: int):
    """assign order to employee"""
    return


@router.post("/orders/{order_id}/schedule")
async def schedule_order(order_id: int):
    """schedule order to employee"""
    return


@router.post("/orders/{order_id}/cancel")
async def cancel_order(order_id: int):
    return