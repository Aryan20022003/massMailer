import smtplib
import json
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os


load_dotenv()

def test():
    arr=[1,2,3,4,5]
    arr1=['a','b','c','d']

    totalCountOfEmails=len(arr)
    senderIdPointer=0
    count=0
    for i in range (totalCountOfEmails-1,-1,-1):
        
        if (count>2):
            count=0
            senderIdPointer=(senderIdPointer+1)%(len(arr1))
        
        print(arr[i],arr1[senderIdPointer])
        arr.pop()
        count+=1
    

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

def sendMail(fromEmail,toEmail,message,server,personGotMail,personNotGotMail):
    message["To"]=toEmail
    try:
        server.sendmail(fromEmail, toEmail, message.as_string())
        personGotMail.append(toEmail)
        print("Email sent to", toEmail)
                
    except Exception as e:
        personNotGotMail.append(toEmail)
        print("Email failed to send to", toEmail)

def appendFile(contents,fileName):
    #open a file in a+ mode and add the contents:arr['stir'] to the fileName if not there then create one 
    with open(fileName,"a+") as f:
        for item in contents:
            f.write(item+"\n")

def mailSender(subject, message_text):
    # Email server settings
    smtp_server = os.getenv("smtp_server")
    smtp_port = os.getenv('port_number')  # For TLS
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    #list of available {userId,password}
    smtp_senderData=list(json.loads(os.getenv("smtp_userData")).items()) #load userId and

    # Email content
    # to_emails = readFileAndReturnList('data.txt')
    to_emails = ["aryannita20022003@gmail.com","aryan20022003@gmail.com"]

    # Create a message object
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg.attach(MIMEText(message_text, "html"))

    personGotMail=[]  
    personNotGotMail=[]

    senderIdPointer=0
    while(True and (len(to_emails)>0)):
        smtp_username = smtp_senderData[senderIdPointer][0]
        smtp_password = smtp_senderData[senderIdPointer][1]
        server.login(smtp_username, smtp_password)
        msg["From"] = smtp_username

        processedTillNow=0
        totalCountOfEmails=len(to_emails)
        # Send the email to each recipient
        for i in range (totalCountOfEmails-1,-1,-1):
            to_email=to_emails[i]

            if (processedTillNow>15):
               processedTillNow=0
               senderIdPointer=(senderIdPointer+1)%(len(smtp_senderData))
               
            sendMail(smtp_username,to_email,msg,server,personGotMail,personNotGotMail)
            to_emails.pop()
            processedTillNow+=1

    # Quit the server
    appendFile(personGotMail,"personGotMail.txt")
    appendFile(personNotGotMail,"personNotGotMail.txt")
    server.quit()


def main():
    subject = "Welcome to Google Cloud Learning Path by GDSC NIT Agartala!"
    messageHtml = markDownToHtml()
    mailSender(subject,messageHtml)

main()


# test()