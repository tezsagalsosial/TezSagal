from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# My first Thread Example
def RegistrationEmailSend(user,link,email):
    email_template = 'email/register.html'
    subject, from_email, to = 'Emailinizi Təstiqləyin zəhmət olmasa', settings.EMAIL_HOST_USER, email
    text_content = 'This is an important message.'
    ctx = {
        'user_full_name': user,
        'confirm_link':link
    }
    message = get_template(email_template).render(ctx)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(message, "text/html")
    msg.send()


def ForgetPasswordSend(user,link, code,email):
    email_template = 'email/forget_password.html'
    subject, from_email, to = 'Şifrənizi dəyişmək üçün kod: %s' % code, settings.EMAIL_HOST_USER, email
    text_content = 'This is an important message.'
    ctx = {
        'user_full_name': user,
        'confirm_link':link,
        'code':code,
    }
    message = get_template(email_template).render(ctx)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(message, "text/html")
    msg.send()

