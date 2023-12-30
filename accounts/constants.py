from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

ACCOUNT_TYPE = (
    ('Reader', 'Reader'),
    ('Author', 'Author'),
)

def send_registration_email(user, subject, template):
        message = render_to_string(template,{
            'user': user,
            'type': user.profile.account_type
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()