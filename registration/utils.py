from django.core.mail import EmailMultiAlternatives

from utilities.commonutils import set_path


def create_email_contents(template_file, name, group, email):
    """
    Accepts a file containing an email template, recipient name,
    group name and recipient email address.
    Returns email content as a string.
    """
    f = open(template_file, 'r')
    template = f.read()
    f.close()

    contents = template.replace('{name}', name, 1)
    contents = contents.replace('{group}', group, 1)
    contents = contents.replace('{email}', email, 1)

    return contents


def send_welcome_email(group, user):
    """
    Sends a welcome email when a user sets up an account.
    """  	
    recipient_email = user.email
    recipient_name = user.first_name
    recipient = [recipient_email]
    bcc = ['welcome@econvenor.org']
    group = group.name

    EMAIL_PATH = set_path('registration/templates/',
        '/home/econvenor/webapps/econvenor/econvenor/registration/templates/')

    text_template_file = EMAIL_PATH + 'welcome_email.txt'
    html_template_file = EMAIL_PATH + 'welcome_email.html'	
    sender = 'eConvenor <mail@econvenor.org>'
    subject = 'Welcome to eConvenor!'
    text_content = create_email_contents(text_template_file, recipient_name,
                                         group, recipient_email)
    html_content = create_email_contents(html_template_file, recipient_name,
                                         group, recipient_email)
    msg = EmailMultiAlternatives(subject, text_content, sender, recipient, bcc)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
