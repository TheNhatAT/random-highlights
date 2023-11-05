import imaplib
import email
from os import environ
import os
from dotenv import load_dotenv

load_dotenv()


# email config
email_address = environ.get("EMAIL_ADDRESS")
email_password = environ.get("EMAIL_PASSWORD")


# TODO: combine this with the handle_highlight function
def handle_read_mails():
    print("email_address", email_address)
    print("email_password", email_password)

    # add try catch
    try:
        # create an IMAP4 class with SSL
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        mail.login(email_address, email_password)

        # select the mailbox you want to delete in

        # if you want SPAM, use "INBOX.SPAM"
        mailbox = "INBOX"
        mail.select(mailbox)

        # get unread mails
        result, data = mail.uid("search", None, "(UNSEEN)")
        print("result", result)
        print("data", data)

        if result == "OK":
            for num in data[0].split():
                result, data = mail.uid("fetch", num, "(BODY[])")
                print("result", result)
                print("data", data)
                if result == "OK":
                    raw_email = data[0][1]
                    # parse the raw email into a readable email object
                    email_message = email.message_from_bytes(raw_email)
                    print("email_message", email_message)
                    # download attachments
                    for part in email_message.walk():
                        if part.get_content_disposition() == "attachment":
                            filename = part.get_filename()
                            if filename:
                                # define subject
                                subject = str(email_message.get("Subject"))
                                if not os.path.isdir(subject):
                                    os.mkdir(subject)
                                filepath = os.path.join(subject, filename)
                                print("filepath", filepath)
                                # download attachment and save it
                                open(filepath, "wb").write(
                                    part.get_payload(decode=True)
                                )
    except Exception as e:
        print(e)
