from .base import Action
from config import SENDGRID_API_KEY, SENDGRID_FROM, SENDGRID_NUMBER_TO_EMAIL_MAP

import sendgrid

class SendGridAction(Action):
    def process(self, subject, body):
        to_emails = SENDGRID_NUMBER_TO_EMAIL_MAP.get(self.from_number)
        if not to_emails:
            return

        sg = sendgrid.SendGridClient(SENDGRID_API_KEY)
        message = sendgrid.Mail()
        message.set_subject(subject)
        message.set_html(body)
        message.set_text(body)
        message.set_from(SENDGRID_FROM)

        for email in to_emails:
            message.add_to(email)

        sg.send(message)
