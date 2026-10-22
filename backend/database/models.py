import decimal
from datetime import datetime

from sqlalchemy import TIMESTAMP, func, ForeignKey, String, Numeric, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .enum import StatusType, MembersRole, CurrencyType, OrderStatusType, KeyStatusType


class Base(DeclarativeBase):
    pass


class Companies(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    active: Mapped[StatusType] = mapped_column(server_default=StatusType.ACTIVE, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
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


class CompanyMembers(Base):
    __tablename__ = "company_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )
    role: Mapped[MembersRole] = mapped_column(
        default=MembersRole.WORKER,
        nullable=False
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
    full_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Services(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(1500), nullable=True)
    base_price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[CurrencyType] = mapped_column(default=CurrencyType.RUB, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(nullable=True)  # время в минутах
    active: Mapped[StatusType] = mapped_column(default=StatusType.ACTIVE, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
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
    created_by: Mapped[int] = mapped_column(ForeignKey("company_members.id"), nullable=False)
    assigned_employee_id: Mapped[int] = mapped_column(
        ForeignKey("company_members.id"), nullable=True
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

    completed_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)


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


class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    hash_refresh_token: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[KeyStatusType] = mapped_column(default=KeyStatusType.ACTIVE, nullable=False)
    expired_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class TelegramAccount(Base):
    __tablename__ = "telegram_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
