from .base import Action
from config import SENDGRID_API_KEY, SENDGRID_FROM
from config import SENDGRID_NUMBER_TO_EMAIL_MAP

import sendgrid


class SendGridAction(Action):
    def process(self, subject, body_text, body_html=''):
        to_emails = SENDGRID_NUMBER_TO_EMAIL_MAP.get(self.from_number)
        if not to_emails:
            return

        subject = subject.format(**locals())
        body_text = body_text.format(**locals())
        body_html = body_html.format(**locals())
        if not body_html:
            body_html = body_text

        sg = sendgrid.SendGridClient(SENDGRID_API_KEY)
        message = sendgrid.Mail()
        message.set_subject(subject)
        message.set_html(body_html)
        message.set_text(body_text)
        message.set_from(SENDGRID_FROM)

        for email in to_emails:
            message.add_to(email)

        sg.send(message)
