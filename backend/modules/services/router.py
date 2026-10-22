from fastapi import APIRouter, Depends, status

from database.enum import MembersRole, StatusType
from database.models import CompanyMembers, Services
from dependencies_factory import check_roles
from modules.services.deps import get_provider_service, check_service_status_type
from modules.services.schema import CreateNewService, UpdateService
from modules.services.service import ProviderService


router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all company services",
)
async def get_company_services(
        company_id: int,
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.get_company_services(company_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new company service",
)
async def create_company_service(
        params: CreateNewService,
        current_member: CompanyMembers = Depends(
            check_roles(
                MembersRole.OWNER,
                MembersRole.MANAGER,
            )
        ),
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.create_new_company_service(params, current_member)


@router.get(
    "/{service_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a company service",
    description="Get a company service by unique ID",
)
async def get_company_service(
        service: Services = Depends(
            check_service_status_type(
                StatusType.ACTIVE,
            )
        ),
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.get_service_by_id(service)


@router.patch(
    "/{service_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a company service",
    description="Update a company service by unique ID",
)
async def patch_company_service(
        params: UpdateService,
        service: Services = Depends(
            check_service_status_type(
                StatusType.ACTIVE,
            )
        ),
        current_member: CompanyMembers = Depends(
            check_roles(
                MembersRole.OWNER,
                MembersRole.MANAGER,
            )
        ),
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.update_company_service(service, params, current_member)


@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a company service",
)
async def delete_company_service(
        service: Services = Depends(
            check_service_status_type(StatusType.ACTIVE)
        ),
        current_member: CompanyMembers = Depends(
            check_roles(
                MembersRole.OWNER,
                MembersRole.MANAGER,
            )
        ),
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.delete_company_service(service, current_member)


@router.patch(
    "/{service_id}/status",
    status_code=status.HTTP_200_OK,
    summary="Patch a company service",
)
async def patch_company_service_status(
        new_status: StatusType,
        service: Services = Depends(
            check_service_status_type(
                StatusType.ACTIVE,
                StatusType.INACTIVE
            )
        ),
        current_member: CompanyMembers = Depends(
            check_roles(
                MembersRole.OWNER,
                MembersRole.MANAGER,
            )
        ),
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.patch_company_service_status(new_status, service, current_member)