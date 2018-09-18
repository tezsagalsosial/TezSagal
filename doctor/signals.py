from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from doctor.models import Doctor
from base_user.tasks import RegistrationEmailSend
from base_user.models import UserConfrimationKeys
from base_user.tools.common import confirmation_link
from threading import Thread

User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid="create_doctor")
def create_doctor(sender,**kwargs):
    user = kwargs.get("instance")

    if user.usertype == 1:
        try:
            Doctor.objects.get(user=user)
            pass
        except:
            Doctor.objects.create(
                user=user,
            )
            pass
    else:
        pass


@receiver(post_save, sender=Doctor, dispatch_uid="confirm_doctor")
def confirm_doctor(sender,**kwargs):
    doctor = kwargs.get("instance")

    if doctor.tesdiq:
        try:
            if not doctor.send_message:
                lock = UserConfrimationKeys.objects.get(user=doctor.user)
                code = lock.key
                link = confirmation_link % ("tezsagal.az", code, doctor.user.id)
                background_send = Thread(target=RegistrationEmailSend,args=(doctor.user.get_full_name(), link, doctor.user.email))
                background_send.start()
                doctor.send_message = True
                doctor.save()
            else:
                pass
        except:
            pass
    else:
        pass
