from django.conf.urls import url
from django.contrib.auth import views as auth_views
from base_user.views import BaseSystemLoginView, NormalUserRegistrationView ,AccountTestView, \
    SendEmailTest, SuccessRegistrationView,RegistrationConfirmationView, RegistrationView, \
    DoctorRegsitrationView, ForgetPasswordView, ChangePasswordView

urlpatterns = [
    url(r'^$', BaseSystemLoginView.as_view(), name="login"),
    url(r'^logout/$', auth_views.logout, name="logout",  kwargs={'next_page': '/'}),
    url(r'^register/$', RegistrationView.as_view(), name="register"),
    url(r'^forget-password/$', ForgetPasswordView.as_view(), name="forget-password"),
    url(r'^forget/$', ChangePasswordView.as_view(), name="forget-form"),
    url(r'^register-user/$', NormalUserRegistrationView.as_view(), name="register-normal"),
    url(r'^register-doctor/$', DoctorRegsitrationView.as_view(), name="register-doctor"),
    url(r'^success/$', SuccessRegistrationView.as_view(), name="success"),
    url(r'^confirmation/$', RegistrationConfirmationView.as_view(), name="confirm-register"),
    # url(r'^check/online/$', AjaxRequestTestingView.as_view(), name="online"),
     # url(r'^', include("news.urls")),
     # Just a testing
    url(r'^test/$', AccountTestView.as_view(), name="test"),
    url(r'^send/$', SendEmailTest.as_view(), name="email-test"),
]