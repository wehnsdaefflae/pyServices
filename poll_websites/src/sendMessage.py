import smtplib
from email.mime.text import MIMEText
from typing import Tuple, Iterable

from src.logger import Logger


def get_config_directory() -> str:
    return "../config/"


def get_data_directory() -> str:
    return "../data/"


def get_credentials() -> Tuple[str, str]:
    with open(get_config_directory() + "/gmail_credentials.txt", mode="r") as file:
        line = file.readline()
        user = line.strip()
        line = file.readline()
        pw = line.strip()
        return user, pw


def send_gmail(recipients: Iterable[str], subject: str, body: str, debug: bool = False):
    recipients_string = ", ".join(recipients)
    Logger.log("Sending {:s} to {:s}:\n{:s}".format(subject, recipients_string, body))

    if debug:
        return

    user, pwd = get_credentials()

    # Prepare actual message
    #message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    #""" % (user, ", ".join(recipient), subject, body)

    # message = f"From: {user:s}\nTo: {recipients_string:s}\nSubject: {subject:s}\n\n{body:s}"
    message = MIMEText(body, "html")
    message["From"] = user
    message["To"] = recipients_string
    message["Subject"] = subject

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(user, pwd)
    server.sendmail(user, recipients, message.as_string())
    server.close()


if __name__ == "__main__":
    send_gmail(["wernsdorfer@gmail.com"], "test sub", "test body", debug=True)
