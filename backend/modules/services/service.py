from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.enum import StatusType
from database.models import Services, CompanyMembers
from modules.services.repository import ProviderRepo
from modules.services.schema import CreateNewService, UpdateService


class ProviderService:
    def __init__(self, session: AsyncSession):
        self.db = session
        self.repo = ProviderRepo(session)

    async def get_company_services(self, company_id: int) -> List:
        services = await self.repo.get_company_service_by_id(company_id)

        return services

    async def create_new_company_service(self, params: CreateNewService, employee: CompanyMembers):
        try:
            service_id = await self.repo.create_company_service(params, employee)
            await self.db.commit()

            return {
                "service_id": service_id,
                "employee full name": f"{employee.first_name} {employee.last_name}",
                "message": "Successfully created new company service"
            }

        except Exception:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create new company service"
            )

    async def get_service_by_id(self, service: Services):
        return service

    async def update_company_service(self, service: Services, params: UpdateService, employee: CompanyMembers):
        if service.company_id != employee.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot change company service"
            )

        try:
            await self.repo.update_company_service(service.id, params)
            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to change company service"
            )
        return {
            "service": service.id,
            "employee": employee.id,
            "message": "Successfully changed company service"
        }

    async def delete_company_service(self, service: Services, employee: CompanyMembers):
        if service.company_id != employee.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot change company service"
            )

        try:
            await self.repo.delete_company_service(service.id)
            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete company service"
            )

        return {
            "service": service.id,
            "employee": employee.id,
            "message": "Successfully deleted company service"
        }

    async def patch_company_service_status(self, new_status: StatusType, service: Services, employee: CompanyMembers):
        if service.company_id != employee.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot change company service"
            )

        try:
            await self.repo.patch_company_service_status(new_status, service.id)
            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to change company service"
            )
