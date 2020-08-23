from typing import Tuple, List
from abc import ABC, abstractmethod
from rolba.record import RecordsCollection
from rolba.email import EmailMessage, EmailSender


class RecordsCollectionsNotifier(ABC):

    @abstractmethod
    def send_notification(self, records_collections: List[Tuple[str, RecordsCollection]]):
        pass


class EmailRecordsCollectionsNotifier(RecordsCollectionsNotifier):

    def __init__(self, email_sender: EmailSender, subscribers_emails: [str], email_subject: str):
        super().__init__()
        self.email_sender = email_sender
        self.subscribers_emails = subscribers_emails
        self.email_subject = email_subject

    def send_notification(self, records_collections: List[Tuple[str, RecordsCollection]]):
        self.email_sender.send_email(
            EmailMessage(
                subject=self.email_subject,
                body=self._get_email_message(records_collections)
            ),
            self.subscribers_emails
        )

    @staticmethod
    def _get_email_message(records_collections: List[Tuple[str, RecordsCollection]]) -> str:
        message = """
        <html>
            <body>
                <h1>Records Notification</h1>
        """
        for collection_name, collection in records_collections:
            message += f"<h2>{collection_name}</h2>"
            if len(collection):
                message += "<ul>"
                for record in collection.get_records():
                    message += f"<li>{record}</li>"
                message += "</ul>"
            else:
                message += "<p>No new records</p>"
        message += """
            </body>
        </html>
        """
        return message
