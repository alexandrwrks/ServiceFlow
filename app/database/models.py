import decimal
from datetime import datetime
from enum import StrEnum

from sqlalchemy import TIMESTAMP, func, ForeignKey, DECIMAL, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Companies(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UserRole(StrEnum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    DISPATCHER = "DISPATCHER"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"
    ACCOUNTANT = "ACCOUNTANT"


class StatusType(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(nullable=False)
    status: Mapped[StatusType] = mapped_column(
        default=StatusType.ACTIVE, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UsersToken(Base):
    __tablename__ = "users_token"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    token_hash: Mapped[str] = mapped_column(nullable=False)
    used: Mapped[bool] = mapped_column(default=False, nullable=False)
    expired_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Employees(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(unique=True, nullable=True)
    status: Mapped[StatusType] = mapped_column(
        default=StatusType.ACTIVE, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Customers(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class CustomerAddresses(Base):
    __tablename__ = "customer_addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)


class Services(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    base_price: Mapped[decimal.Decimal] = mapped_column(nullable=False)
    estimated_duration: Mapped[int] = mapped_column(nullable=False)  # время в минутах
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


class OrderStatusType(StrEnum):
    NEW = "NEW"
    CONFIRMED = "CONFIRMED"
    ASSIGNED = "ASSIGNED"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    INVOICED = "INVOICED"
    PAID = "PAID"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


class CurrencyType(StrEnum):
    RUB = "RUB"


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    status: Mapped[OrderStatusType] = mapped_column(
        default=OrderStatusType.NEW, nullable=False
    )
    description: Mapped[str] = mapped_column(nullable=True)
    total_amount: Mapped[decimal.Decimal] = mapped_column(nullable=True)
    currency: Mapped[CurrencyType] = mapped_column(
        default=CurrencyType.RUB, nullable=True
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assigned_employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    completed_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )


class OrderHistoryStatus(Base):
    __tablename__ = "order_history_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    old_status: Mapped[OrderStatusType] = mapped_column(nullable=True)
    new_status: Mapped[OrderStatusType] = mapped_column(nullable=False)
    changed_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )


class VisitStatusType(StrEnum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    scheduled_start: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    scheduled_end: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    actual_start: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    actual_end: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    status: Mapped[VisitStatusType] = mapped_column(
        default=VisitStatusType.SCHEDULED, nullable=True
    )
    address: Mapped[int] = mapped_column(
        ForeignKey("customer_addresses.id"), nullable=True
    )
    notes: Mapped[str] = mapped_column(nullable=True)


class QuantityType(StrEnum):
    UNIT = "UNIT"


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit: Mapped[QuantityType] = mapped_column(
        default=QuantityType.UNIT, nullable=False
    )
    minimum_quantity: Mapped[int] = mapped_column(nullable=True)


class InventoryItemMovement(StrEnum):
    RECEIPT = "RECEIPT"  # получение / добавление(нового) на склад
    CONSUMPTION = "CONSUMPTION"  # использование
    RETURN = "RETURN"  # возврат на склад
    ADJUSTMENT = "ADJUSTMENT"  # списание


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id: Mapped[int] = mapped_column(primary_key=True)
    inventory_item_id: Mapped[int] = mapped_column(
        ForeignKey("inventory_items.id"), nullable=False
    )
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    movement_type: Mapped[InventoryItemMovement] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )


class InvoiceStatusType(StrEnum):
    DRAFT = "DRAFT"  # черновик, черновой вариант
    ISSUED = "ISSUED"  # выпущенный, выданный
    PAID = "PAID"  # оплаченный
    CANCELLED = "CANCELLED"  # отменённый


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    total: Mapped[decimal.Decimal] = mapped_column(nullable=False)
    currency: Mapped[CurrencyType] = mapped_column(
        default=CurrencyType.RUB, nullable=False
    )
    status: Mapped[InvoiceStatusType] = mapped_column(nullable=False)
    paid_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)


class NotificationStatusType(StrEnum):
    CREATED = "CREATED"
    SENT = "SENT"


class ChannelType(StrEnum):
    EMAIL = "EMAIL"
    TELEGRAM = "TELEGRAM"


class NotificationType(StrEnum):
    ORDER_ASSIGNED = "ORDER_ASSIGNED"  # назначенный заказ
    INVENTORY_UPDATE = (
        "ORDER_ASSIGNED"  # обновление инвентаря (пополнение, возвращение и др)
    )
    SERVICE_ASSIGNED = "SERVICE_ASSIGNED"  # появление нового заказа


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    channel: Mapped[ChannelType] = mapped_column(nullable=False)
    type: Mapped[NotificationType] = mapped_column(nullable=False)
    status: Mapped[NotificationStatusType] = mapped_column(
        default=NotificationStatusType.CREATED, nullable=False
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    sent_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)


class KeyStatusType(StrEnum):
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"


class ApiKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    key_hash: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[KeyStatusType] = mapped_column(
        default=KeyStatusType.ACTIVE, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )


class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    hash_refresh_token: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[KeyStatusType] = mapped_column(default=KeyStatusType.ACTIVE, nullable=False)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=func.now(), nullable=False)
    revoked_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)