from __future__ import annotations

import email
import imaplib
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from typing import List


@dataclass
class MailCredentials:
    address: str
    password: str


@dataclass
class InboxMessage:
    uid: str
    sender: str
    subject: str
    body_preview: str


class EmailClient:
    def __init__(self, smtp_server: str, smtp_port: int, imap_server: str, imap_port: int):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.imap_server = imap_server
        self.imap_port = imap_port

    def send_email(self, creds: MailCredentials, to: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = creds.address
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=20) as server:
            server.starttls()
            server.login(creds.address, creds.password)
            server.send_message(message)

    def fetch_inbox(self, creds: MailCredentials, limit: int = 5) -> List[InboxMessage]:
        with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as mailbox:
            mailbox.login(creds.address, creds.password)
            mailbox.select("INBOX")
            _, data = mailbox.search(None, "ALL")
            all_uids = data[0].split()
            latest_uids = list(reversed(all_uids[-limit:]))

            messages: List[InboxMessage] = []
            for uid in latest_uids:
                _, msg_data = mailbox.fetch(uid, "(RFC822)")
                raw = msg_data[0][1]
                parsed = email.message_from_bytes(raw)

                sender = parsed.get("From", "Unknown sender")
                subject = parsed.get("Subject", "No subject")
                body = self._extract_body(parsed)
                messages.append(
                    InboxMessage(
                        uid=uid.decode(),
                        sender=sender,
                        subject=subject,
                        body_preview=(body[:120] + "...") if len(body) > 120 else body,
                    )
                )
            return messages

    def delete_email(self, creds: MailCredentials, uid: str) -> None:
        with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as mailbox:
            mailbox.login(creds.address, creds.password)
            mailbox.select("INBOX")
            mailbox.store(uid, "+FLAGS", "\\Deleted")
            mailbox.expunge()

    def reply_email(self, creds: MailCredentials, to: str, subject: str, body: str) -> None:
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"
        self.send_email(creds, to, subject, body)

    @staticmethod
    def _extract_body(parsed_message: email.message.Message) -> str:
        if parsed_message.is_multipart():
            for part in parsed_message.walk():
                content_type = part.get_content_type()
                disposition = str(part.get("Content-Disposition", ""))
                if content_type == "text/plain" and "attachment" not in disposition:
                    payload = part.get_payload(decode=True) or b""
                    return payload.decode(errors="ignore").strip()
            return ""

        payload = parsed_message.get_payload(decode=True) or b""
        return payload.decode(errors="ignore").strip()
