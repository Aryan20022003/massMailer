# Email Sender Script

This is a Python script for sending emails to a list of recipients using the SMTP protocol. It can be used for various purposes like sending newsletters, announcements, or any other bulk email operations.

## Prerequisites

Before using this script, make sure you have the following prerequisites:

- Python 3.x
- Required Python packages (install them using `pip`):
  - `smtplib`
  - `markdown`
  - `python-dotenv`

## Configuration

1. Create a `.env` file in the project directory and configure the following variables:

   ```
   smtp_server=your_smtp_server
   port_number=your_smtp_port
   smtp_userData={"user1": "password1", "user2": "password2", ...}
   ```

   Replace `your_smtp_server`, `your_smtp_port`, `user1`, `password1`, `user2`, `password2`, etc., with your SMTP server details and email credentials.

2. Create a `data.txt` file in the project directory containing the list of recipient email addresses, one per line.

## Usage

1. Run the `main()` function in the script to send emails to the list of recipients specified in `data.txt`.

   ```python
   def main():
       subject = "Welcome to Google Cloud Learning Path by GDSC NIT Agartala!"
       messageHtml = markDownToHtml()
       mailSender(subject, messageHtml)

   main()
   ```

2. The script will send emails in batches, rotating through different SMTP accounts specified in the `.env` file.

3. User id is generally the email address itself (e.g,user1@google.com) and for password you have to generate an app password from your google account.

   - Go to [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Select app as mail and device as other
   - Copy the generated password and paste it in the `.env` file
   - For other email providers, you can follow the same steps.

## Customization

- You can customize the email subject and message content by modifying the `subject` and `messageHtml` variables in the `main()` function.
- Adjust the batch size and other email sending parameters as needed in the `mailSender()` function.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [python-dotenv](https://pypi.org/project/python-dotenv/) - For loading environment variables from a `.env` file.
- [Markdown](https://pypi.org/project/Markdown/) - For converting Markdown content to HTML.
- [smtplib](https://docs.python.org/3/library/smtplib.html) - Python's built-in library for sending emails using SMTP.

