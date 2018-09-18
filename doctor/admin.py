from django.contrib import admin
from doctor.models import BaseContact, BaseSlider, DoctorBlog, Doctor, BlogTv,Currency,WorkCountry, \
    Xestelik, Country, PaymentModel, SponsorModel, MeetingModels, Banner, BlogComment, DoctorXestelik, StaticPage,PaymentWorkCountry
from django.contrib.auth import get_user_model
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.flatpages.models import FlatPage
from django import forms

# Note: we are renaming the original Admin and Form as we import them!
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld


User = get_user_model()

# Register your models here.
class BaseContactsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'locations')
    search_fields = ('email',)



class DoctorAdmin(admin.ModelAdmin):
    readonly_fields = ('get_user_full_name','get_user_diplom','get_user_email')
    fields = ('user','get_user_full_name','work_country','get_user_diplom','get_user_email','tesdiq', 'payment_status','position','rate',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user','reference','description','prize','status','base_date')

class SponsorAdmin(admin.ModelAdmin):
    list_display = ('doctor','place','prize','status','base_date')

class WorkCountryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {"slug": ("name",)}



admin.site.register(BaseContact, BaseContactsAdmin)
admin.site.register(BaseSlider)
admin.site.register(DoctorBlog)
admin.site.register(Xestelik)
admin.site.register(PaymentWorkCountry)
# admin.site.register(DoctorXestelik)
admin.site.register(Country)
admin.site.register(Currency)
admin.site.register(WorkCountry, WorkCountryAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(BlogTv)
admin.site.register(PaymentModel, PaymentAdmin)
admin.site.register(SponsorModel, SponsorAdmin)
admin.site.register(MeetingModels)
admin.site.register(Banner)
admin.site.register(BlogComment)
admin.site.register(StaticPage)



from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _

# Define a new FlatPageAdmin
class FlatPage2Form(forms.ModelForm):
    # content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = FlatPage
        widgets = {
            'content': CKEditorUploadingWidget(config_name='default'),
        }
        fields = '__all__'
        fieldsets = (
            (None, {'fields': ('url', 'title', 'content', 'sites')}),
            (_('Advanced options'), {
                'classes': ('collapse', ),
                'fields': (
                    'enable_comments',
                    'registration_required',
                    'template_name',
                ),
            }),
        )

class FlatPage2Admin(admin.ModelAdmin):
    form = FlatPage2Form
# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPage2Admin)



# from cked.widgets import CKEditorWidget
# from django.contrib import admin
# from django.contrib.flatpages.admin import FlatPageAdmin
# from django.contrib.flatpages.models import FlatPage
# from django.db import models
# class FlatPageCustom(FlatPageAdmin):
#     formfield_overrides = {
#         models.TextField: {'widget': CKEditorWidget}
#     }
#
# admin.site.unregister(FlatPage)
# admin.site.register(FlatPage, FlatPageCustom)

# class FlatpageForm(FlatpageFormOld):
#     content = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = FlatPage # this is not automatically inherited from FlatpageFormOld
#
#
# class FlatPageAdmin(FlatPageAdminOld):
#     form = FlatpageForm
#
#
# # We have to unregister the normal admin, and then reregister ours
# # admin.site.unregister(FlatPage)
# admin.site.register(FlatPage, FlatPageAdmin)


