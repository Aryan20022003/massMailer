import smtplib
import json
import time
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
    return content


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
        time.sleep(7) #wait for 7 sec to look like human
                
    except Exception as e:
        personNotGotMail.append(toEmail)
        print("Email failed to send to", toEmail)

def appendFile(contents,fileName):
    #open file in a+ and populate the file
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
    if (len(smtp_senderData)==0):
        print("No sender data found")
        return
    elif (len(smtp_senderData)==1):
        print("if you send more than 25-30 mail then mailId quality will degrade")
        print("So please add more than 1 mailId")
        response=input("Do you want to continue? (y/n)")
        if (response=="n"):
            return
    # Email content
    to_emails = readFileAndReturnList('data.txt')
    # to_emails = ["aryannita20022003@gmail.com"]

    # Create a message object
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg.attach(MIMEText(message_text, "html"))

    #store the list of person who got mail and who not got mail
    personGotMail=[]  
    personNotGotMail=[]

    senderIdPointer=0
    while(True and (len(to_emails)>0)):
        smtp_username = smtp_senderData[senderIdPointer][0]
        smtp_password = smtp_senderData[senderIdPointer][1]
        server.login(smtp_username, smtp_password)
        msg["From"] = smtp_username
        print("Sending mail from",smtp_username)
        processedTillNow=0
        totalCountOfEmails=len(to_emails)
        # Send the email to each recipient
        for i in range (totalCountOfEmails-1,-1,-1):
            to_email=to_emails[i]

            if (processedTillNow>25):
               processedTillNow=0
               senderIdPointer=(senderIdPointer+1)%(len(smtp_senderData))
               break
               
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