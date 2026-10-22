from fastapi import APIRouter, Depends, status

from database.models import CompanyMembers, MembersRole, OrderStatusType
from dependencies_factory import check_roles

from modules.employees.deps import check_roles_without_company_id
from modules.order.deps import get_order_service, ExistsOrder
from modules.order.schema import OrderParams
from modules.order.service import OrderService


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_orders(
        params: OrderParams,
        current_member: CompanyMembers = Depends(
            check_roles_without_company_id(
                MembersRole.OWNER,
                MembersRole.MANAGER
            )
        ),
        service: OrderService = Depends(get_order_service)
):
    return await service.create_order(params, current_member)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all orders"
)
async def get_orders(
        current_member: CompanyMembers = Depends(
            check_roles(
                MembersRole.OWNER,
                MembersRole.MANAGER
            )
        ),
        service: OrderService = Depends(get_order_service)
):
    return await service.get_orders(current_member)


@router.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    summary="Get order info"
)
async def get_order(
        order: ExistsOrder,
        current_member: CompanyMembers = Depends(
            check_roles(
                MembersRole.OWNER,
                MembersRole.MANAGER
            )
        ),
        service: OrderService = Depends(get_order_service)
):
    return await service.get_order_by_id(order, current_member)


@router.patch(
    "/{order_id}/status",
    status_code=status.HTTP_200_OK,
)
async def update_order_status(
        order: ExistsOrder,
        new_status: OrderStatusType,
        current_member: CompanyMembers = Depends(
            check_roles_without_company_id(
                MembersRole.OWNER,
                MembersRole.MANAGER,
                MembersRole.WORKER
            )
        ),
        service: OrderService = Depends(get_order_service)
):
    return await service.update_order_status(order.id, current_member, new_status)


@router.get(
    "/{order_id}/history",
    status_code=status.HTTP_200_OK,
    summary="Get order history"
)
async def get_history(
        order: ExistsOrder,
        current_member: CompanyMembers = Depends(
            check_roles_without_company_id(
                MembersRole.OWNER,
                MembersRole.MANAGER
            )
        ),
        service: OrderService = Depends(get_order_service)
):
    return await service.get_order_history(order, current_member)


@router.post(
    "/{order_id}/assign_employee",
    status_code=status.HTTP_201_CREATED,
    summary="Assign employee to order"
)
async def assign_employee(
        order: ExistsOrder,
        assigned_employee_id: int,
        current_member: CompanyMembers = Depends(
            check_roles_without_company_id(
                MembersRole.OWNER,
                MembersRole.MANAGER
            )
        ),
        service: OrderService = Depends(get_order_service)
):
    return await service.assigned_employee(order, assigned_employee_id, current_member)