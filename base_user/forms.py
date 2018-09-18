from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import authenticate

from PIL import Image

# get custom user
User = get_user_model()


class MyUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_(
                                             "Raw şifrələr bazada saxlanmır, onları heç cürə görmək mümkün deyil "
                                             "bu istifadəçinin şifrəsidir, lakin siz onu dəyişə bilərsiziniz "
                                             " <a href=\"../password/\">bu form</a>. vasitəsilə"))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


"""
    ################################################################################################
    Base System For Client Login -----------------------------------------------------------------------
    ################################################################################################
"""


class BaseAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label="İstifadəçi adı")
    password = forms.CharField(label="Parol", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(BaseAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(attrs={
            'placeholder': _("E-poçt"), 'class': 'form-control form-project', 'id': 'user_email', 'autofocus': None})
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'placeholder': _("Şifrə"), 'class': 'form-control form-project', 'id': 'user_password'})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Təəsüflər olsunki email və ya şifrə yanlışdır")
        return user


class UserRegistrationBaseView(forms.Form):
    name = forms.CharField(max_length=254, label="Adı", error_messages={})
    surname = forms.CharField(max_length=254, label="Soyadı", error_messages={})
    email = forms.EmailField(error_messages={})
    password = forms.CharField(label=_("Parol"))
    retype_password = forms.CharField(label=_("Parol yeniden"))

    def __init__(self, *args, **kwargs):
        super(UserRegistrationBaseView, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'placeholder': _("Ad")})
        self.fields['surname'].widget = forms.TextInput(attrs={
            'placeholder': _("Soyad")})
        self.fields['email'].widget = forms.EmailInput(attrs={
            'placeholder': _("Email")})
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'placeholder': _("Şifrə")})
        self.fields['retype_password'].widget = forms.PasswordInput(attrs={
            'placeholder': _("Şifrənin təsdiqi")})

    def clean(self):
        cleaned_data = super(UserRegistrationBaseView, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('retype_password')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(_("Şifrə təstiqlənməsi alınmadı"))
        return cleaned_data

    def save(self, commit=True):
        name = self.cleaned_data.get('name')
        surname = self.cleaned_data.get('surname')
        username = self.cleaned_data.get('email')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if commit:
            user = User.objects.create_user(
                first_name=name,
                last_name=surname,
                email=email,
                username=username,
                password=password,
            )
            user.is_active = False
            user.save()
            return user
        else:
            return forms.ValidationError(_("Password beraber deyil"))

CHOSE = (
    (1, "Kişi"),
    (2, "Qadın")
)

class DoctorRegistrationBaseView(forms.Form):
    name = forms.CharField(max_length=254, label="Adı", error_messages={})
    surname = forms.CharField(max_length=254, label="Soyadı", error_messages={})
    father_name = forms.CharField(max_length=254, label=_("Ata adı"), error_messages={})
    diplom_number = forms.CharField(max_length=254, label=_("Ata adı"), error_messages={})
    gender = forms.ChoiceField(choices=CHOSE)
    email = forms.EmailField(error_messages={})
    password = forms.CharField(label=_("Parol"))
    retype_password = forms.CharField(label=_("Parol yeniden"))

    def __init__(self, *args, **kwargs):
        super(DoctorRegistrationBaseView, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'placeholder': _("Ad")})
        self.fields['surname'].widget = forms.TextInput(attrs={
            'placeholder': _("Soyad")})
        self.fields['father_name'].widget = forms.TextInput(attrs={
            'placeholder': _("Ata adı")})
        self.fields['diplom_number'].widget = forms.NumberInput(attrs={
            'placeholder': _("Diplom nömrəsi")})
        self.fields['email'].widget = forms.EmailInput(attrs={
            'placeholder': _("Email")})
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'placeholder': _("Şifrə")})
        self.fields['retype_password'].widget = forms.PasswordInput(attrs={
            'placeholder': _("Şifrənin təsdiqi")})

    def clean(self):
        cleaned_data = super(DoctorRegistrationBaseView, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('retype_password')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(_("Şifrə təstiqlənməsi alınmadı"))
        return cleaned_data

    def save(self, commit=True):
        name = self.cleaned_data.get('name')
        surname = self.cleaned_data.get('surname')
        username = self.cleaned_data.get('email')
        father_name = self.cleaned_data.get('father_name')
        diplom_number = self.cleaned_data.get('diplom_number')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if commit:
            user = User.objects.create_user(
                first_name=name,
                last_name=surname,
                father_name=father_name,
                diplom_number=diplom_number,
                email=email,
                username=username,
                password=password,
            )
            user.is_active = False
            user.save()
            return user
        else:
            return forms.ValidationError(_("Password beraber deyil"))


class ChangePasswordForm(forms.Form):
    code = forms.CharField(max_length=6)
    password = forms.CharField(label=_("Parol"))
    retype_password = forms.CharField(label=_("Parol yeniden"))

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget = forms.PasswordInput(attrs={
            'placeholder': _("Təhlükəsizlik kodu")})
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'placeholder': _("Yeni Şifrə")})
        self.fields['retype_password'].widget = forms.PasswordInput(attrs={
            'placeholder': _("Yeni Şifrənin təsdiqi")})

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('retype_password')
        code = cleaned_data.get('code')
        user = User.objects.get(code=code)
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(_("Şifrə təsdiqlənməsi alınmadı"))
            else:
                user.set_password(password)
                user.save()
        return user