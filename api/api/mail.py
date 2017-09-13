from flask import render_template
from flask_mail import Mail, Message
from .app import app


mail = Mail(app)


def send_mail(template, recipients, **kwargs):
    html = render_template('email/' + template + '.html', **kwargs)
    text = render_template('email/' + template + '.txt', **kwargs)
    subject = render_template('email/' + template + '.subject', **kwargs)
    message = Message(
        body=text, recipients=recipients, html=html, subject=subject)
    mail.send(message)
