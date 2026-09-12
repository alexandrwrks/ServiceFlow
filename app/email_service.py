from email.message import EmailMessage

import aiosmtplib

from app.utils.settings import settings


class EmailService:

    async def send_employee_invitation(self, email: str, token: str) -> None:

        message = EmailMessage()

        message["From"] = settings.EMAIL_FROM
        message["To"] = email
        message["Subject"] = "Приглашение в ServiceFlow"

        activation_url = (
            f"{settings.FRONTEND_URL}/employees/invitations/{token}/activate"
        )

        message.set_content(
            f"""
Здравствуйте!

Вас пригласили в ServiceFlow.

Для активации аккаунта перейдите по ссылке:

{activation_url}

После перехода необходимо установить собственный пароль.

Если вы не ожидали это письмо, просто проигнорируйте его.
"""
        )

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=465,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            use_tls=True,
        )

        print("Письмо успешно отправлено через Mail.ru!")
