from email.message import EmailMessage
import smtplib
import os

def send_email(to_address: str, subject: str, body: str) -> bool:
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    smtp_use_tls = os.environ.get("SMTP_USE_TLS", "true").lower() in ("true", "1", "yes")

    if not smtp_host or not smtp_user or not smtp_pass:
        print("SMTP not configured; email not sent.")
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = smtp_user
    message["To"] = to_address
    message.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            if smtp_use_tls:
                smtp.starttls()
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(message)
        return True
    except Exception as exc:
        print("Error sending email:", exc)
        return False