from django.contrib.sites.models import Site
from django.db import models
from django.urls import get_script_prefix
from django.utils.encoding import iri_to_uri

from doctor.options.tools import get_base_slider, get_base_blog, slugify, PAYMENT_TYPE, \
    MONEY_TYPE
from django.utils import timezone

from geoposition.fields import GeopositionField
# from geoposition import Geoposition
# from django.contrib.auth import get_user_model
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class BaseContact(models.Model):
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Əsas telefon")
    email = models.EmailField(null=True, blank=True, verbose_name="Əsas email")
    facebook = models.URLField(null=True, blank=True, verbose_name="facebook linki")
    twitter = models.URLField(null=True, blank=True, verbose_name="twitter linki")
    linkedin = models.URLField(null=True, blank=True, verbose_name="linkedin linki")
    instagram = models.URLField(null=True, blank=True, verbose_name="instagram linki")
    pinterest = models.URLField(null=True, blank=True, verbose_name="pinterest linki")
    locations = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ərazi haqqında")
    phone1 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Əlaqə nömrəsi 1")
    phone2 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Əlaqə nömrəsi 2")
    email1 = models.EmailField(null=True, blank=True, verbose_name="Əlavə email 1")
    email2 = models.EmailField(null=True, blank=True, verbose_name="Əlavə email 2")

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Əsas kontakt'
        verbose_name_plural = 'Əsas kontaktlar'

    def __str__(self):
        return "%s %s %s %s" % (self.phone, self.email, self.locations, self.facebook)


class BaseSlider(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="Başlıq")
    sub_title = models.CharField(max_length=255, null=True, blank=True, verbose_name="Alt mövzu")
    description = models.TextField(null=True, blank=True, verbose_name="Təsvir")
    image = models.ImageField(upload_to=get_base_slider, verbose_name="Şəkil")
    status = models.BooleanField(default=True, verbose_name="Saytda görünüşü")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Slayder'
        verbose_name_plural = 'Slayderlər'

    def __str__(self):
        return "%s" % self.title


class ContactMessages(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Adı")
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon")
    message = models.TextField(null=True, blank=True, verbose_name="Mesaj")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Mesaj'
        verbose_name_plural = 'Mesajlar'

    def __str__(self):
        return self.name

class Banner(models.Model):
    name = models.CharField(max_length=255, null=True,blank=True)
    picture = models.ImageField(upload_to='banners/')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.name

class Currency(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255,unique=True)
    symbol = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class WorkCountry(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    # quantity = models.DecimalField(max_digits=19, decimal_places=2)
    # currency = models.ForeignKey('Currency')
    def __str__(self):
        return self.name

class PaymentWorkCountry(models.Model):
    title = models.CharField(max_length=255)
    work_country = models.ForeignKey('WorkCountry')
    month_count = models.IntegerField()
    quantity = models.FloatField(default=0)
    currency = models.ForeignKey('Currency')
    def __str__(self):
        return self.work_country.name
    class Meta:
        unique_together = (("work_country", "month_count"),)
        ordering = ['month_count']

class Doctor(models.Model):
    user = models.ForeignKey('base_user.MyUser')
    base_name = models.CharField(max_length=255, null=True,blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    work_country = models.ForeignKey('WorkCountry', null=True, blank=True)
    qebul_qiymeti = models.IntegerField(null=True, blank=True)
    prize_type = models.CharField(choices=MONEY_TYPE, max_length=100,null=True, blank=True)
    pasient_types = models.CharField(max_length=255, null=True, blank=True)
    work_place = models.CharField(max_length=255, null=True, blank=True)
    position = GeopositionField(blank=True,null=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    twitter_link = models.CharField(max_length=255, null=True, blank=True)
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.TimeField(default=timezone.now)
    end_date = models.TimeField(default=timezone.now)
    step_1 = models.BooleanField(default=False)
    step_2 = models.BooleanField(default=False)
    step_3 = models.BooleanField(default=False)
    step_4 = models.BooleanField(default=False)
    step_5 = models.BooleanField(default=False)
    rate = models.DecimalField(max_digits=19, decimal_places=5,default=0.0)
    rate_general_rate = models.DecimalField(max_digits=19, decimal_places=5,default=0.0)
    rate_spend_time = models.DecimalField(max_digits=19, decimal_places=5,default=0.0)
    rate_working_politeness = models.DecimalField(max_digits=19, decimal_places=5,default=0.0)
    rate_diagnosis = models.DecimalField(max_digits=19, decimal_places=5,default=0.0)
    rate_follow_after_examination = models.DecimalField(max_digits=19, decimal_places=5,default=0.0)
    rate_registration_status = models.DecimalField(max_digits=19, decimal_places=5,default=0.0)
    rate_office_status = models.DecimalField(max_digits=19, decimal_places=5,default=0.0)
    rate_prepare_paying_process = models.DecimalField(max_digits=19, decimal_places=5,default=0.0)

    education = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    job_description = models.TextField(null=True,blank=True)
    goals = models.TextField(null=True,blank=True)
    cv = models.FileField(null=True,blank=True)
    tesdiq = models.BooleanField(default=False)
    send_message = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False, verbose_name="Ödəniş statusu")
    payment_date = models.DateTimeField(null=True,blank=True, verbose_name="Ödəniş Tarixi")


    def __str__(self):
        return "%s" % self.user.get_full_name()

    def check_status(self):
        if self.step_1 and not self.step_2:
            return 20
        elif self.step_1 and self.step_2 and not self.step_3:
            return 40
        elif self.step_1 and self.step_2 and self.step_3 and not self.step_4:
            return 60
        elif self.step_1 and self.step_2 and self.step_3 and self.step_4 and not self.step_5:
            return 80
        elif self.step_1 and self.step_2 and self.step_3 and self.step_4 and self.step_5:
            return 100


    def get_author_name(self):
        return "%s" % (self.user.get_full_name())

    def get_user_full_name(self):
        return "%s %s" % (self.user.get_full_name(), self.user.father_name)

    get_user_full_name.short_description = "Həkimin tam adı"
    get_user_full_name.allow_tags = True

    def get_user_diplom(self):
        return "%s" % self.user.diplom_number

    get_user_diplom.short_description = "Diplomun nömrəsi"
    get_user_diplom.allow_tags = True

    def get_user_email(self):
        return "%s" % self.user.email

    get_user_full_name.short_description = "Elektron poçtu"
    get_user_full_name.allow_tags = True

    def get_country_list(self):
        try:
            d = DoctorCountry.objects.filter(doctor=self)
            if d:
                arr = [z for z in d]
                return arr
            else:
                return False
        except:
            return False

    def get_xestelik(self):
        try:
            d = DoctorXestelik.objects.filter(doctor=self)
            if d:
                arr = [z for z in d]
                return arr
            else:
                return False
        except:
            return False

    def get_doctor_time(self):
        try:
            if DoctorTimeTable.objects.filter(doctor=self).last():
                data = DoctorTimeTable.objects.filter(doctor=self)
                arr = [d.time.strftime('%m/%d/%Y') for d in data]
                return arr
        except:
            return False




class DoctorTimeTable(models.Model):
    doctor = models.ForeignKey('Doctor')
    time = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Həkimin cədvəli'

    def __str__(self):
        return "%s" % self.doctor.user.get_full_name()


class DoctorBlog(models.Model):
    title = models.CharField(max_length=255, verbose_name="Başlıq")
    author = models.ForeignKey('Doctor')
    image = models.ImageField(upload_to=get_base_blog, null=True, blank=True, verbose_name="Şəkil")
    text = RichTextUploadingField(config_name='default')
    slug = models.SlugField(null=True,blank=True)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Bloq'
        verbose_name_plural = 'Bloqlar'

    def __str__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        super(DoctorBlog, self).save(*args, **kwargs)
        self.slug = slugify(self.title)
        super(DoctorBlog, self).save(*args, **kwargs)


class BlogComment(models.Model):
    user = models.ForeignKey('base_user.MyUser')
    doctor = models.ForeignKey('Doctor', null=True, blank=True)
    star = models.IntegerField(default=0)
    diagnosis = models.IntegerField(default=0)
    spend_time = models.IntegerField(default=0)
    follow_after_examination = models.IntegerField(default=0)
    registration_status = models.IntegerField(default=0)
    working_politeness = models.IntegerField(default=0)
    office_status = models.IntegerField(default=0)
    prepare_paying_process = models.IntegerField(default=0)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Rəy'
        verbose_name_plural = 'Rəylər'

    def __str__(self):
        return "%s" % self.text


class BlogTv(models.Model):
    url = models.URLField()
    date = models.DateTimeField(auto_now_add=True)


class Xestelik(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Xəstəlik'
        verbose_name_plural = 'Xəstəliklər'

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Şəhər'
        verbose_name_plural = 'Şəhərlər'

    def __str__(self):
        return self.name

class DoctorXestelik(models.Model):
    doctor = models.ForeignKey('Doctor',null=True, blank=True)
    xestelik = models.ForeignKey('Xestelik')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.xestelik.name


class DoctorCountry(models.Model):
    doctor = models.ForeignKey('Doctor', null=True, blank=True)
    country = models.ForeignKey('Country')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.country.name


class PaymentModel(models.Model):
    user = models.ForeignKey('base_user.MyUser')
    reference = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    prize = models.FloatField(default=0)
    data = models.TextField()
    status = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    base_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "%s" % self.user.get_full_name()


class SponsorModel(models.Model):
    doctor = models.ForeignKey('Doctor')
    place = models.IntegerField(null=True, blank=True)
    prize = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=False)
    base_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "%s" % self.doctor.user.get_full_name()


class MeetingModels(models.Model):
    user = models.ForeignKey('base_user.MyUser')
    doctor = models.ForeignKey('Doctor')
    meet_date = models.ForeignKey('DoctorTimeTable', null=True, blank=True)
    meet_time = models.DateTimeField(default=timezone.now)
    question = models.BooleanField(default=False)
    text = models.TextField(default="")
    tarix = models.TimeField(default=timezone.now)
    payment = models.IntegerField(choices=PAYMENT_TYPE, default=2)
    status = models.BooleanField(default=False)
    is_accept = models.CharField(max_length=20,default='waiting')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.user.get_full_name(), self.doctor.user.get_full_name())

class StaticPage(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = RichTextUploadingField(config_name='default')
    enable_comments = models.BooleanField(_('enable comments'), default=False)
    template_name = models.CharField(
        _('template name'),
        max_length=70,
        blank=True,
        help_text=_(
            "Example: 'staticpages/contact_page.html'. If this isn't provided, "
            "the system will use 'staticpages/default.html'."
        ),
    )
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=_("If this is checked, only logged-in users will be able to view the page."),
        default=False,
    )
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))

    class Meta:
        # db_table = 'django_staticpage'
        verbose_name = _('static page')
        verbose_name_plural = _('static pages')
        ordering = ('url',)

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)

    # def get_absolute_url(self):
    #     # Handle script prefix manually because we bypass reverse()
    #     return iri_to_uri(get_script_prefix().rstrip('/') + self.url)