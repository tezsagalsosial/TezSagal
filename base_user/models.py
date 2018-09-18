from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from base_user.tools.common import get_user_profile_photo_file_name, GENDER, USERTYPES, slugify
from datetime import datetime as d
import calendar
from django.db.models import Q
# My custom tools import



# Create your models here.
USER_MODEL = settings.AUTH_USER_MODEL
import random


# Customize User model
class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    username = models.CharField(_('username'), max_length=100, unique=True,
                                help_text=_('Tələb olunur. 75 simvol və ya az. Hərflər, Rəqəmlər və '
                                            '@/./+/-/_ simvollar.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$', _('Düzgün istifadəçi adı daxil edin.'),
                                                              'yanlışdır')
                                ])
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), max_length=255)
    birthday = models.DateField(verbose_name="ad günü", default=timezone.now)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    diplom_number = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=get_user_profile_photo_file_name, null=True, blank=True)
    profile_picture_1 = models.ImageField(upload_to=get_user_profile_photo_file_name, null=True, blank=True)
    profile_picture_2 = models.ImageField(upload_to=get_user_profile_photo_file_name, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, verbose_name="cinsi", default=1)
    verified = models.BooleanField(default=False, verbose_name="Təstiqlənmə")
    code = models.CharField(max_length=20,null=True,blank=True, verbose_name="Kod")
    unvani = models.CharField(max_length=255, verbose_name="ünvanı", null=True, blank=True)
    phone = models.CharField(max_length=100, verbose_name="Telefonu", null=True, blank=True)
    study = models.CharField(max_length=200, verbose_name="Təhsili", null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)



    usertype = models.IntegerField(choices=USERTYPES, verbose_name="Sistemdəki statusu", null=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    """
        Important non-field stuff
    """
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def save(self, *args, **kwargs):
        super(MyUser, self).save(*args, **kwargs)
        self.slug = slugify(self.first_name.replace("İ", "i")+str(timezone.now().timestamp()).replace('.','-'))
        super(MyUser, self).save(*args, **kwargs)


class UserConfrimationKeys(models.Model):
    key = models.CharField(max_length=255,null=True, blank=True)
    user = models.ForeignKey('MyUser', null=True,blank=True)
    expired = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
        verbose_name = "Təstiqlənmiş user"
        verbose_name_plural = "Təstiqlənmiş userlər"

    def __str__(self):
        return "%s" % self.key