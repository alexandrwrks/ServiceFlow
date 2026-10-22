from enum import StrEnum


class StatusType(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class MembersRole(StrEnum):
    OWNER = "OWNER"  # основатель компании
    ADMIN = "ADMIN"  # админ
    MANAGER = "MANAGER"  # менеджер
    WORKER = "WORKER"  # сотрудник


EMPLOYEES_ROLES = {
    MembersRole.MANAGER,
    MembersRole.WORKER
}


class CurrencyType(StrEnum):
    RUB = "RUB"


class OrderStatusType(StrEnum):
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    INVOICED = "INVOICED"
    PAID = "PAID"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


class KeyStatusType(StrEnum):
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
