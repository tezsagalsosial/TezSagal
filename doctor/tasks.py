from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# My first Thread Example
def MeetingRequestToDoctor(doctor,meet):
    email_template = 'email/meet_request.html'
    subject, from_email, to = 'Hörmətli %s həkim, %s %s sizin pasient qəbulunuz istənilir' % (doctor.user.first_name,meet.meet_time.strftime("%m/%d/%Y"), meet.tarix.strftime("%H:%M")), settings.EMAIL_HOST_USER, doctor.user.email
    text_content = 'This is an important message.'
    ctx = {
        'hekim_adi': doctor.user.first_name,
        'tarix': meet.meet_time.strftime("%m/%d/%Y"),
        'saat': meet.tarix.strftime("%H:%M"),
        'xeste_get_full_name': meet.user.get_full_name,
        'mesaj' : meet.text,
        'status' : "Kartla ödəniş" if meet.status else "Nəğd ödəniş",
        'xeste_email': meet.user.email,
    }
    message = get_template(email_template).render(ctx)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(message, "text/html")
    msg.send()

    # email_template2 = 'email/meet_response.html'
    # subject2, from_email, to2 = 'Siz  %s  %s tarixində, %s  həkimin qəbuluna yazıldınız' % (meet.meet_time.strftime("%m/%d/%Y"), meet.tarix.strftime("%H:%M"),meet.doctor.user.first_name), settings.EMAIL_HOST_USER, meet.user.email
    # # text_content = 'This is an important message.'
    # ctx2 = {
    #     'hekim_adi': meet.doctor.user.first_name,
    #     'tarix': meet.meet_time.strftime("%m/%d/%Y"),
    #     'saat': meet.tarix.strftime("%H:%M")
    # }
    # message = get_template(email_template2).render(ctx2)
    # msg2 = EmailMultiAlternatives(subject2, text_content, from_email, [to2])
    # msg2.attach_alternative(message, "text/html")
    # msg2.send()


# My first Thread Example
def MeetingResponseToPasient(meet):
    email_template2 = 'email/meet_response.html'
    subject2, from_email, to2 = 'Siz  %s  %s tarixində, %s  həkimin qəbuluna yazıldınız' % (meet.meet_time.strftime("%m/%d/%Y"), meet.tarix.strftime("%H:%M"),meet.doctor.user.first_name), settings.EMAIL_HOST_USER, meet.user.email
    text_content = 'This is an important message.'
    ctx2 = {
        'hekim_adi': meet.doctor.user.first_name,
        'tarix': meet.meet_time.strftime("%m/%d/%Y"),
        'saat': meet.tarix.strftime("%H:%M")
    }
    message = get_template(email_template2).render(ctx2)
    msg2 = EmailMultiAlternatives(subject2, text_content, from_email, [to2])
    msg2.attach_alternative(message, "text/html")
    msg2.send()


def ReviewMessages(doctor, meet,url):
    email_template = 'email/review_sms.html'
    subject, from_email, to = 'Zəhmət olmasa görüşü dəyərləndirin' , settings.EMAIL_HOST_USER, meet.email
    text_content = 'This is an important message.'
    ctx = {
        'hekim': doctor.user.first_name,
        'confirm_link': url
    }
    message = get_template(email_template).render(ctx)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(message, "text/html")
    msg.send()
