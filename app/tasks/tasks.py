import asyncio

from app.email_service import EmailService
from app.tasks.broker import broker


@broker.task(retry_on_error=True,)
async def send_email_invitations(email: str, token: str) -> None:
    print(f"[RabbitMQ] Отправка сообщения на {email}")

    email_service = EmailService()

    await email_service.send_employee_invitation(
        email=email,
        token=token
    )