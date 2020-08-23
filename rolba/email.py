import smtplib
import ssl
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailMessage:

    def __init__(self, subject: str, body: str):
        self.subject = subject
        self.body = body

    def get_subject(self) -> str:
        return self.subject

    def get_body(self) -> str:
        return self.body


class EmailSender(ABC):

    @abstractmethod
    def send_email(self, email: EmailMessage, recipients: [str]):
        pass


class SimpleSmtpEmailSender(EmailSender):

    def __init__(self, smtp_url: str, user: str, password: str):
        self.smtp_url = smtp_url
        self.user = user
        self.password = password

    def send_email(self, email: EmailMessage, recipients: [str]):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_url, 465, context=context) as server:
            server.login(self.user, self.password)
            message = MIMEMultipart()
            message["Subject"] = email.get_subject()
            message["From"] = self.user
            message["To"] = ", ".join(recipients)
            message.attach(MIMEText(email.get_body(), "html"))
            server.sendmail(
                from_addr=self.user,
                to_addrs=recipients,
                msg=message.as_string()
            )
