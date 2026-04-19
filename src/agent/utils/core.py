from email.message import Message

from langchain_core.documents import Document


def make_content_text(
    subject: str,
    from_val: str,
    to_val: str,
    date: str,
    content: str
) -> str:
    return "\n".join((
        f"Subject: {subject}",
        f"From: {from_val}",
        f"To: {to_val}",
        f"Date: {date}",
        f"Content: {content}"
    ))

def make_email_document(msg: Message) -> Document:
    content = "Unknown"

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                content = part.get_payload(decode=True).decode()
    else:
        content = msg.get_payload(decode=True).decode()

    return Document(page_content=make_content_text(
        subject=msg.get("Subject", "Unknown"),
        from_val=msg.get("From", "Unknown"),
        to_val=msg.get("To", "Unknown"),
        date=msg.get("Date", "Unknown"),
        content=content
    ))
