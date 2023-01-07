import smtplib, email, imaplib, time
import imaplib
import email
from bs4 import BeautifulSoup
import openai
import smtplib

openai.api_key = "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"

# Open the file in read-only mode
with open('ai_mis_en_situation.txt', 'r') as file:
    # Read the contents of the file into a string
    ai_mis_en_situation = file.read() + " "
    # Open the file in read-only mode
with open('ai_mis_en_situation_2.txt', 'r') as file:
    # Read the contents of the file into a string
    ai_mis_en_situation_2 = file.read() + " "
    # Open the file in read-only mode
with open('company_termsconditions.txt', 'r') as file:
    # Read the contents of the file into a string
    company_termsconditions = file.read() + " "

def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = ai_mis_en_situation + company_termsconditions + ai_mis_en_situation_2 + prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.5,
    )

    message = completions.choices[0].text
    return message

# Replace with your email address and password
EMAIL_ADDRESS = 'customer.service.128ver1@gmail.com'
EMAIL_PASSWORD = 'jprypawfcypcvhhd'

def send_email(from_addr, password, to_addr, message):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login('customer.service.128ver1@gmail.com', 'jprypawfcypcvhhd')

        subject_write = 'Re: '

        msg_write = f'Subject: {subject_write}\n\n{message}'

        smtp.sendmail('customer.service.128ver1@gmail.com', to_addr, msg_write)

imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
imap_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

while True:
    # Check for new emails.
    imap_server.select('inbox')
    status, messages = imap_server.search(None, 'UNSEEN')
    if status != "OK":
        print("Error searching for new emails.")
        continue

    # Get the list of email IDs.
    email_ids = messages[0].split()

    # Loop through the messages
    for message_id in messages[0].split():
        # Fetch the message
        status, msg = imap_server.fetch(message_id, '(RFC822)')

        # Parse the message
        msg = email.message_from_bytes(b'' + msg[0][1])

        # Print the sender and subject
        print(f'From: {msg["From"]}')
        print(f'Subject: {msg["Subject"]}')
        sender_read = msg["From"]
        subject_read = msg["Subject"]

        # Check if the message is multipart
        if msg.is_multipart():
            # Loop through the message parts
            for part in msg.walk():
                # Get the content type
                content_type = part.get_content_type()

                # Check if the content type is text/html
                if content_type == 'text/html':
                    # Get the message body
                    body = part.get_payload(decode=True)

                    # Convert the HTML to plain text
                    soup = BeautifulSoup(body, 'html.parser')
                    text = soup.get_text()
                    body_write = generate_response(text)
                    print(body_write)
        else:
            # Get the message body
            body = msg.get_payload(decode=True)
            body_write = generate_response(text)
            print(body_write)


        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login('customer.service.128ver1@gmail.com', 'jprypawfcypcvhhd')

            subject_write = 'Re: ' + subject_read

            msg_write = f'Subject: {subject_write}\n\n{body_write}'

            smtp.sendmail('customer.service.128ver1@gmail.com', sender_read, msg_write)

    # command = input('Type "stop" to stop the loop: ')
    # if command == 'stop':
    #     # Close the mailbox
    #     imap_server.close()
    #     # Logout
    #     imap_server.logout()

    #     break
