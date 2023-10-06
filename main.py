import smtplib
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()


def readFileAndReturnList(path):
    with open(path) as f:
        content = f.readlines()

    content = [x[:-1] for x in content]
    content[-1] = content[-1] + "m"
    print(content)


def markDownToHtml():
    with open("content.md") as f:
        content = f.read()
    content = markdown.markdown(content)
    return content


def mailSender(
    smtp_server, user_name, user_password, from_email, subject, message_text
):
    # Email server settings
    smtp_port = 25  # For TLS
    smtp_username = user_name
    smtp_password = user_password

    # Create an SMTP object
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Email content
    # to_emails = readFileAndReturnList('data.txt')
    to_emails = ["aryannita20022003@gmail.com"]
    # Create a message object
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message_text, "html"))

    # Send the email to each recipient
    for to_email in to_emails:
        msg["To"] = to_email
        try:
            server.sendmail(from_email, to_email, msg.as_string())
            print("Email sent to", to_email)
            
        except Exception as e:
            print("Email failed to send to", to_email)
    # Quit the server
    server.quit()


def main():
    subject = "Welcome to Google Cloud Learning Path by GDSC NIT Agartala!"
    messageHtml = markDownToHtml()
    smtp_server = os.getenv("smtp_server")
    user_name = os.getenv("user_name")
    user_password = os.getenv("user_password")
    from_email = os.getenv("from_email")
    mailSender(smtp_server, user_name, user_password,from_email,subject,messageHtml)


main()
