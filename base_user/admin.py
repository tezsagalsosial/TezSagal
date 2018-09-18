from django.contrib import admin
from base_user.models import MyUser
from base_user.forms import MyUserChangeForm, MyUserCreationForm
from base_user.models import UserConfrimationKeys
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

# Admin panel actions here
def make_verified_doctor(modeladmin, request, queryset):
    queryset.update(verified=True)


make_verified_doctor.short_description = "Həkimləri təstiqlə"


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
        'first_name', 'last_name', 'email', 'username', 'birthday', 'gender', 'unvani', 'phone', 'study',
        'profile_picture', 'usertype')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("first_name", "last_name", 'username', 'password1', 'password2'),
        }),
    )
    # The forms to add and change user instances
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
    actions = [make_verified_doctor]


admin.site.register(User, MyUserAdmin)
admin.site.register(UserConfrimationKeys)
