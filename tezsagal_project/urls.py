"""tezsagal_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils import translation
from django.views import generic
from doctor.paymen_views import BasePaymentCheckView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^payments/', BasePaymentCheckView.as_view(), name='payment-check'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^e8b138ed91cf.html$', generic.TemplateView.as_view(template_name='e8b138ed91cf.html'), name='site-verification-com'),
    url(r'^e6e7c523116a.html$', generic.TemplateView.as_view(template_name='e6e7c523116a.html'), name='site-verification-az'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

translation.activate(settings.LANGUAGE_CODE)

urlpatterns += i18n_patterns(
    url(r'^', include("doctor.urls", namespace="base")),
    url(r'^pages/', include('django.contrib.flatpages.urls'), name='flat'),
    url(r'^account/', include("base_user.urls", namespace="account")),
)
