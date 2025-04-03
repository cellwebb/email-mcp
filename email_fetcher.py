import imaplib
import email
import os
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

def connect_to_email():
    """Connect to email server and return IMAP object."""
    mail = imaplib.IMAP4_SSL(os.getenv("EMAIL_SERVER"), int(os.getenv("EMAIL_PORT")))
    mail.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
    return mail

def fetch_emails(limit=10):
    """Fetch latest emails and return structured data."""
    mail = connect_to_email()
    mail.select("INBOX")
    
    # Get latest emails
    status, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    
    # Take only the most recent emails
    recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
    
    emails = []
    for e_id in recent_ids:
        status, data = mail.fetch(e_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Get email details
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        
        from_ = decode_header(msg["From"])[0][0]
        if isinstance(from_, bytes):
            from_ = from_.decode()
        
        # Get email body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        body = "Unable to decode body"
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        
        emails.append({
            "id": e_id.decode(),
            "subject": subject,
            "from": from_,
            "body": body[:500] + ("..." if len(body) > 500 else ""),  # Truncate long bodies
            "date": msg["Date"]
        })
    
    mail.close()
    mail.logout()
    return emails

def delete_email(email_id):
    """Delete an email by its ID."""
    mail = connect_to_email()
    mail.select("INBOX")
    
    # Mark email as deleted
    mail.store(email_id.encode(), '+FLAGS', '\\Deleted')
    
    # Expunge to actually delete
    mail.expunge()
    
    mail.close()
    mail.logout()
    return f"Email {email_id} deleted successfully"

if __name__ == "__main__":
    emails = fetch_emails(5)
    for i, email in enumerate(emails, 1):
        print(f"--- Email {i} ---")
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Date: {email['date']}")
        print(f"Body: {email['body'][:100]}...")
        print()
