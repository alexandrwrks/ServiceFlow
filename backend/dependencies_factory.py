from fastapi import Depends, HTTPException, status

from database.models import MembersRole, Users, CompanyMembers, StatusType
from modules.auth.deps import get_current_user
from modules.companies.deps import get_company_repo
from modules.companies.repo import CompanyRepo


def check_roles(*allowed_roles: MembersRole):
    async def role_checker(
            company_id: int,
            current_user: Users = Depends(get_current_user),
            repo: CompanyRepo = Depends(get_company_repo)
    ) -> CompanyMembers:
        member = await repo.get_company_member(company_id, current_user.id)

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь не является участником компании"
            )

        if member.status != StatusType.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Сотрудник не активен"
            )

        if member.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав"
            )

        return member
    return role_checker