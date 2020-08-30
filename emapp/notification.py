import uuid
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage


from flask import current_app


ICAL_TEMPLATE = u'''
BEGIN:VCALENDAR
VERSION:2.0
PRODID:emapp
BEGIN:VEVENT
DTEND:{end_time}
DTSTART:{start_time}
SUMMARY:{event_name}
UID:{uid}
END:VEVENT
END:VCALENDAR
'''


class Notification:
    def __init__(self, event, signup_email):
        self.event = event
        self.signup_email = signup_email

    def send_signup_email(self):
        msg = EmailMessage()
        msg.set_content((
            'User {} just signed up for '
            'the event {} (id={}) from {} to {}.').format(
            self.signup_email, self.event['name'], self.event['id'],
            self.event['start_time'], self.event['end_time']))
        msg['Subject'] = '{} signed up the event {}'.format(
            self.signup_email, self.event['name'])
        config = current_app.config['NOTIFICATION']
        msg['From'] = config['signup_email_from']
        msg['To'] = config['signup_email_to']
        with smtplib.SMTP(**config['smtp_server']) as s:
            s.send_message(msg)

    def send_invitation(self):
        msg = MIMEMultipart()
        config = current_app.config['NOTIFICATION']
        msg['From'] = config['invitation_email_from']
        msg['To'] = self.signup_email
        msg['Subject'] = 'Invitation to event {}'.format(self.event['name'])
        msg.attach(
            MIMEText('You can add the following attachment to the calendar.'))
        attachment = MIMEBase(
            'text', 'calendar; name=invite.ics; method=REQUEST; charset=UTF-8')
        ics = ICAL_TEMPLATE.format(
            uid=uuid.uuid1(),
            event_name=self.event['name'],
            start_time=self.event['start_time'].strftime(r'%Y%m%dT%H%M%SZ'),
            end_time=self.event['end_time'].strftime(r'%Y%m%dT%H%M%SZ'),
        )
        attachment.set_payload(ics.encode('utf-8'))
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition',
                              'attachment; filename={}'.format('calendar.ics'))
        msg.attach(attachment)
        with smtplib.SMTP(**config['smtp_server']) as s:
            s.send_message(msg)
