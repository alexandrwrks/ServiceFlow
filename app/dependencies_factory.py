from fastapi import Depends, HTTPException, status

from app.database.models import UserRole, Users
from app.modules.auth.deps import get_current_user


def check_roles(*allowed_roles: UserRole):
    async def role_checker(
            current_user: Users = Depends(get_current_user)
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав"
            )

        return current_user

    return role_checker