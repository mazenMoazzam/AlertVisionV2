import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("SMTP_EMAIL")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def send_email(image_files):
    if not image_files:
        print("No images to send, skipping email.")
        return

    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = RECIPIENT_EMAIL
    message["Subject"] = "AlertVision Detection Alert – Human Detected"

    body = "Attached are frames where human detection occurred."
    message.attach(MIMEText(body, "plain"))

    for image in image_files:
        with open(image, "rb") as file:
            img = MIMEImage(file.read())
            img.add_header("Content-Disposition", f"attachment; filename={os.path.basename(image)}")
            message.attach(img)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, message.as_string())
        print(f"Email sent successfully with {len(image_files)} images.")
    except Exception as e:
        print(f"Failed to send email: {e}")
