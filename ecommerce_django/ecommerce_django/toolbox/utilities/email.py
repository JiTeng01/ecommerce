from django.core.mail import send_mail, EmailMessage
from django.template import loader, Context
import os


def send_email(subject, message, sender, recipients, template, context):
    html_message = loader.get_template(template).render(context)
    return send_mail(subject=subject, message=message, html_message=html_message, from_email=sender,
                     recipient_list=recipients)


def send_email_attachment(subject, message, from_email, attached_file, recipients, content_type=None,
                          email_template=None, email_data=None):
    if email_template:
        message = loader.get_template(email_template).render(Context(email_data))
    mail = EmailMessage(subject=subject, body=message, from_email=from_email, to=recipients)
    mail.content_subtype = 'html'
    if os.path.exists(attached_file):
        file_content = open(attached_file, 'r').read()
        mail.attach(os.path.basename(attached_file), file_content, content_type)
        mail.send()
