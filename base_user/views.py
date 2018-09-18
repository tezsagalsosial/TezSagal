from django.shortcuts import render, render_to_response, redirect
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
# from django.views.generic import TemplateView, FormView, ListView, CreateView, UpdateView, DetailView,DeleteView
from django.urls import reverse
# from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import FormView, TemplateView, View
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from base_user.tools.decorator import LoginRequiredMixinView
from base_user.tools.common import id_generator, confirmation_link, change_pass, forget_link
from base_user.forms import BaseAuthenticationForm, UserRegistrationBaseView, ChangePasswordForm, \
    DoctorRegistrationBaseView
from base_user.tasks import RegistrationEmailSend, ForgetPasswordSend
from base_user.models import UserConfrimationKeys
from doctor.views import TezsagalBaseView

from threading import Thread
# import os
# import datetime
# import random
# from django.conf import settings
# from django.db.models import Q

User = get_user_model()


# THis is a test view for show template
class AccountTestView(TemplateView):
    template_name = 'accounts/registration/register_normal.html'


# Create your views here.
class BaseSystemLoginView(LoginRequiredMixinView, TezsagalBaseView, FormView):
    model = User
    form_class = BaseAuthenticationForm
    template_name = 'accounts/login/login.html'
    login_template = 'development/base/index.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.cleaned_data
        if user.usertype == 1:
            login(self.request, user)
            return redirect(reverse('base:dashboard'))
        else:
            login(self.request, user)
            return redirect(reverse("base:index"))



    def form_invalid(self, form):
        messages.success(
            self.request, 'Email və ya şifrə yanlışdır'
        )
        return redirect(reverse('account:login'))

    def get_context_data(self, **kwargs):
        context = super(BaseSystemLoginView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


class NormalUserRegistrationView(TezsagalBaseView,FormView):
    model = User
    template_name = 'accounts/registration/register_normal.html'
    form_class = UserRegistrationBaseView
    success_url = '/'
    success_html = 'accounts/success/success_index.html'

    def form_valid(self, form):
        user = form.save()
        user.usertype = 2
        user.save()
        code = id_generator()
        key = UserConfrimationKeys(
            user=user,
            key=code,
        )
        key.save()
        link = confirmation_link % (self.request.META['HTTP_HOST'],code,user.id)
        background_send = Thread(target=RegistrationEmailSend,args=(user.get_full_name, link, user.email))
        background_send.start()
        messages.success(
            self.request, _("%s, saytda qeydiyyatdan keçdiyiniz üçün təşəkkür edirik. Qeydiyyatınızın təsdiqlənməsi üçün zəhmət olmasa, %s poçt ünvanınızı yoxlayın." % (user.get_full_name(), user.email))
        )
        return redirect(reverse("account:success"))

    def form_invalid(self, form):
        messages.success(
            self.request, str(form.errors)
        )
        return redirect(reverse("account:register-normal"))

    def get_context_data(self, **kwargs):
        context = super(NormalUserRegistrationView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


class DoctorRegsitrationView(TezsagalBaseView,FormView):
    model = User
    template_name = 'accounts/registration/register_doctor.html'
    form_class = DoctorRegistrationBaseView
    success_url = '/'
    success_html = 'accounts/success/success_index.html'

    def form_valid(self, form):
        user = form.save()
        user.usertype = 1
        user.save()
        code = id_generator()
        key = UserConfrimationKeys(
            user=user,
            key=code,
        )
        key.save()
        link = confirmation_link % (self.request.META['HTTP_HOST'],code,user.id)
        # background_send = Thread(target=RegistrationEmailSend,args=(user.get_full_name, link, user.email))
        # background_send.start()
        messages.success(
            self.request, _("Təşəkkür edirik Hörmətli %s, Qeydiyyatınız uğurla tamamlandı zəhmət olmasa adminin təsdiqindən sonra %s poçtunuzu yoxlayın, və profilinizi doldurun" % (user.get_full_name(),user.email))
        )
        return redirect(reverse("account:success"))

    def form_invalid(self, form):
        messages.success(
            self.request, str(form.errors)
        )
        return redirect(reverse("account:register-normal"))

    def get_context_data(self, **kwargs):
        context = super(DoctorRegsitrationView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


class ForgetPasswordView(View):
    template_name = 'accounts/forget_password/forget.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):
        try:
            code = change_pass()
            get_email = request.POST.get('email')
            user = User.objects.get(email=get_email)
            user.code = code
            user.save()
            domain_name = request.META['HTTP_HOST']
            link = forget_link % (domain_name, code)
            send_message = Thread(target=ForgetPasswordSend, args=(user.get_full_name,link,code,user.email))
            send_message.start()
            messages.success(
                self.request, _("Zəhmət olmasa %s elektron poçtunuzu yoxlayın" % user.email)
            )
            return redirect(reverse("account:forget-form"))
        except:
            messages.success(
                self.request, _("%s adında email sistemdə yoxdur" % request.POST.get('email'))
            )
            return redirect(reverse("account:success"))


class ChangePasswordView(TezsagalBaseView, FormView):
    model = User
    form_class = ChangePasswordForm
    template_name = 'accounts/forget_password/forget_form.html'
    login_template = 'development/base/index.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.cleaned_data
        login(self.request, user)
        return redirect(reverse('base:index'))

    def form_invalid(self, form):
        messages.success(
            self.request, 'Email və ya şifrə yanlışdır'
        )
        return redirect(reverse('account:forget-form'))

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['code'] = self.request.GET.get('code','')
        return context


class SuccessRegistrationView(TezsagalBaseView,TemplateView):
    template_name = 'accounts/success/success_index.html'


class RegistrationView(TezsagalBaseView, TemplateView):
    template_name = 'accounts/registration/register.html'

class RegistrationConfirmationView(TemplateView, View):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user')
        code = request.GET.get('code')
        key = UserConfrimationKeys.objects.get(key=code,user_id=user_id)
        key.expired = True
        key.save()
        base_user = User.objects.get(id=user_id)
        base_user.is_active = True
        base_user.save()
        if base_user.usertype == 1:
            login(request, base_user)
            return redirect('base:dashboard')
        elif base_user.usertype == 2:
            login(request, base_user)
            return redirect('base:index')


# Email send testing
class SendEmailTest(View):
    email_template = 'email/register.html'

    def get(self,request):
        background_send = Thread(target=RegistrationEmailSend, args=('Munis Isazade','http://localhost:8023/az/','munisisazade@gmail.com'))
        background_send.start()
        return HttpResponse("Email ugurla gonderildi")