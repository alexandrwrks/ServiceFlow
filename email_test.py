import asyncio

from backend.email_service import EmailService


if __name__ == "__main__":
    email_service = EmailService()
    asyncio.run(
        email_service.send_employee_invitation(
            email="koozma-alex@mail.ru",
            token="adagwagrh"
        )
    )