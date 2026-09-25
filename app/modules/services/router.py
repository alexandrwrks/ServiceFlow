from fastapi import APIRouter, Depends

from app.database.models import Users, UserRole
from app.dependencies_factory import check_roles
from app.modules.services.deps import get_provider_service
from app.modules.services.schema import CreateNewService, UpdateService
from app.modules.services.service import ProviderService


router = APIRouter(prefix="/services")


@router.get("/")
async def get_company_services(
        company_id: int,
        service: ProviderService = Depends(get_provider_service)
):
    return await service.get_company_services(company_id)


@router.post("/")
async def create_company_service(
        params: CreateNewService,
        current_employee: Users = Depends(
            check_roles(
                UserRole.OWNER,
                UserRole.MANAGER,
                UserRole.ADMIN,
            )
        ),
        service: ProviderService = Depends(get_provider_service)
):
    return await service.create_new_company_service(params, current_employee)


@router.get("/{service_id}")
async def get_company_service(
        service_id: int,
        service: ProviderService = Depends(get_provider_service)
):
    return await service.get_service_by_id(service_id)


@router.patch("/{service_id}")
async def patch_company_service(
        service_id: int,
        params: UpdateService,
        current_employee: Users = Depends(
            check_roles(
                UserRole.OWNER,
                UserRole.MANAGER,
                UserRole.ADMIN,
            )
        ),
        service: ProviderService = Depends(get_provider_service)
):
    return await service.change_company_service(service_id, params, current_employee)


@router.delete("/{service_id}")
async def delete_company_service(
        service_id: int,
        current_employee: Users = Depends(
            check_roles(
                UserRole.OWNER,
                UserRole.MANAGER,
                UserRole.ADMIN,
            )
        ),
        service: ProviderService = Depends(get_provider_service)
):
    return await service.delete_company_service(service_id, current_employee)


@router.patch("/{service_id}/status")
async def patch_company_service_status(
        service_id: int,
        current_employee: Users = Depends(
            check_roles(
                UserRole.OWNER,
                UserRole.MANAGER,
                UserRole.ADMIN,
            )
        ),
        service: ProviderService = Depends(get_provider_service)
):
    return await service.patch_company_service_status(service_id, current_employee)