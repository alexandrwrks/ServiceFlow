from fastapi import APIRouter, Depends

from app.database.models import Users, UserRole
from app.dependencies_factory import check_roles
from app.modules.services.deps import get_provider_service, CheckServiceIdDep
from app.modules.services.schema import CreateNewService, UpdateService
from app.modules.services.service import ProviderService


router = APIRouter(prefix="/services")


@router.get("/")
async def get_company_services(
        company_id: int,
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.get_company_services(company_id)


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
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.create_new_company_service(params, current_employee)


@router.get("/{service_id}")
async def get_company_service(
        service: CheckServiceIdDep,
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.get_service_by_id(service)


@router.patch("/{service_id}")
async def patch_company_service(
        service: CheckServiceIdDep,
        params: UpdateService,
        current_employee: Users = Depends(
            check_roles(
                UserRole.OWNER,
                UserRole.MANAGER,
                UserRole.ADMIN,
            )
        ),
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.update_company_service(service, params, current_employee)


@router.delete("/{service_id}")
async def delete_company_service(
        service: CheckServiceIdDep,
        current_employee: Users = Depends(
            check_roles(
                UserRole.OWNER,
                UserRole.MANAGER,
                UserRole.ADMIN,
            )
        ),
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.delete_company_service(service, current_employee)


@router.patch("/{service_id}/status")
async def patch_company_service_status(
        service: CheckServiceIdDep,
        current_employee: Users = Depends(
            check_roles(
                UserRole.OWNER,
                UserRole.MANAGER,
                UserRole.ADMIN,
            )
        ),
        manager: ProviderService = Depends(get_provider_service)
):
    return await manager.patch_company_service_status(service.id, current_employee)