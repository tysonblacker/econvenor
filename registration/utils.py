from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_welcome_email(group, user):
    """
    Sends a welcome email when a user sets up an account.
    """

    recipient_email = user.email
    recipient_name = user.first_name
    recipient = [recipient_email]
    bcc = ['welcome@econvenor.org']
    group = group.name

    sender = 'eConvenor <mail@econvenor.org>'
    subject = 'Welcome to eConvenor!'
    text_content = render_to_string(
        'welcome_email.txt',
        {
            'name': recipient_name,
            'group': group,
            'email': recipient_email,
        }
    )
    html_content = render_to_string(
        'welcome_email.html',
        {
            'name': recipient_name,
            'group': group,
            'email': recipient_email,
        }
    )

    msg = EmailMultiAlternatives(subject, text_content, sender, recipient, bcc)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
