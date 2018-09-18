from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, FormView, DetailView, ListView
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from geoposition import Geoposition

from doctor.models import BaseContact, ContactMessages, BaseSlider, DoctorBlog, BlogTv, \
    Xestelik, Country, Doctor, DoctorXestelik, DoctorCountry, DoctorTimeTable, \
    SponsorModel, MeetingModels, BlogComment, Banner, StaticPage,PaymentWorkCountry
from doctor.forms import LeaveMessageForm, ChangePictureForm, \
    DashboardPersonalForm, BlogAddForm, PositionForm
from doctor.options.decorators import LoginRestrictedMixin
from doctor.tasks import MeetingRequestToDoctor, ReviewMessages ,MeetingResponseToPasient

from datetime import datetime
from threading import Thread
# import datetime
# from dateutil.relativedelta import relativedelta


User = get_user_model()

class TezsagalGeneralView(View):
    def get_context_data(self, **kwargs):
        context = super(TezsagalGeneralView, self).get_context_data(**kwargs)
        context['static_pages'] = StaticPage.objects.all()
        return context


# Create your views here.
class TezsagalBaseView(View):
    def get_nav_menu_contacts(self):
        obj = BaseContact.objects.all().last()
        return obj

    def get_context_data(self, **kwargs):
        context = super(TezsagalBaseView, self).get_context_data(**kwargs)
        context['base_menu_contact'] = self.get_nav_menu_contacts()
        context['static_pages'] = StaticPage.objects.all()
        return context


class BaseIndexView(TezsagalBaseView, TemplateView):
    template_name = 'production/main_index/home.html'

    def get_slider(self):
        obj = BaseSlider.objects.filter(status=True)
        return obj

    def get_context_data(self, **kwargs):
        context = super(BaseIndexView, self).get_context_data(**kwargs)
        context['slider'] = self.get_slider()
        doc_ils = DoctorXestelik.objects.all()
        doc_ils_list = [int(x.xestelik.id) for x in doc_ils]
        context['ill'] = Xestelik.objects.filter(id__in=doc_ils_list)
        context['country'] = Country.objects.all()
        return context


class DashboardView(LoginRestrictedMixin,
                    TezsagalBaseView,
                    TemplateView):
    template_name = 'production/dashboard/dashboard_base.html'
    my_form = DashboardPersonalForm
    success_url = ''

    def post(self, request, *args, **kwargs):
        doctors = get_object_or_404(Doctor,user=request.user)
        xestelikler = request.POST.getlist('ilness')
        sheherler = request.POST.getlist('area')
        if xestelikler:
            for id in xestelikler:
                try:
                    DoctorXestelik.objects.get(xestelik_id=id, doctor=doctors)
                    pass
                except:
                    xes = DoctorXestelik(
                        xestelik_id=id,
                        doctor=doctors
                    )
                    xes.save()
        if sheherler:
            for y in sheherler:
                try:
                    DoctorCountry.objects.get(country_id=y, doctor=doctors)
                    pass
                except:
                    sheh = DoctorCountry(
                        country_id=y,
                        doctor=doctors
                    )
                    sheh.save()
        if not doctors.step_1:
            doctors.phone = request.POST.get('phone', '')
            doctors.prize_type = request.POST.get('prize_type', '')
            doctors.facebook_link = request.POST.get('facebook_link', '')
            doctors.twitter_link = request.POST.get('twitter_link', '')
            doctors.instagram_link = request.POST.get('instagram_link', '')
            doctors.base_name = request.POST.get('base_name', '')
            doctors.language = request.POST.get('language', '')
            if request.POST.get('qebul_qiymeti'):
                doctors.qebul_qiymeti = request.POST.get('qebul_qiymeti')
            else:
                doctors.qebul_qiymeti = 0
            doctors.pasient_types_az = request.POST.get('pasient_types_az', '')
            doctors.pasient_types_ru = request.POST.get('pasient_types_ru', '')
            doctors.pasient_types_ka = request.POST.get('pasient_types_ka', '')
            doctors.description_az = request.POST.get('personal_info_az', '')
            doctors.description_ru = request.POST.get('personal_info_ru', '')
            doctors.description_ka = request.POST.get('personal_info_ka', '')
            position_lat = request.POST.get('position_0')
            position_lon = request.POST.get('position_1')
            if position_lat:
                latitude = position_lat
            else:
                latitude = 0
            if position_lon:
                longitude = position_lon
            else:
                longitude = 0
            doctors.position = Geoposition(latitude, longitude)
            doctors.step_1 = True
            doctors.save()
            return redirect(reverse('base:dashboard-education'))
        else:
            doctors.phone = request.POST.get('phone', '')
            doctors.facebook_link = request.POST.get('facebook_link', '')
            doctors.prize_type = request.POST.get('prize_type', '')
            doctors.twitter_link = request.POST.get('twitter_link', '')
            doctors.instagram_link = request.POST.get('instagram_link', '')
            doctors.base_name = request.POST.get('base_name', '')
            doctors.language = request.POST.get('language', '')
            if request.POST.get('qebul_qiymeti'):
                doctors.qebul_qiymeti = request.POST.get('qebul_qiymeti')
            else:
                doctors.qebul_qiymeti = 0
            doctors.pasient_types_az = request.POST.get('pasient_types_az', '')
            doctors.pasient_types_ru = request.POST.get('pasient_types_ru', '')
            doctors.pasient_types_ka = request.POST.get('pasient_types_ka', '')
            doctors.description_az = request.POST.get('personal_info_az', '')
            doctors.description_ru = request.POST.get('personal_info_ru', '')
            doctors.description_ka = request.POST.get('personal_info_ka', '')
            position_lat = request.POST.get('position_0')
            position_lon = request.POST.get('position_1')
            if position_lat:
                latitude = position_lat
            else:
                latitude = 0
            if position_lon:
                longitude = position_lon
            else:
                longitude = 0
            # latitude = 0

            # return HttpResponse(businnes_type)
            # i = 1
            # for pos in position_get:
            #     if i == 1:
            #         latitude = Decimal(pos)
            #     if i == 2:
            #         longitude = Decimal(pos)
            #     i += 1
            doctors.position = Geoposition(latitude, longitude)
            doctors.save()
            return redirect(reverse('base:dashboard-education'))

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        doctor = get_object_or_404(Doctor,user=self.request.user)

        context['ill'] = Xestelik.objects.all()
        context['country'] = Country.objects.all()
        context['doctor'] = doctor
        try:
            context['positionform'] = PositionForm(initial={
                'position': Geoposition(doctor.position.latitude, doctor.position.longitude)
            })
        except:
            context['positionform'] = PositionForm()
        return context


# # Check user online or not
# class AjaxRequestTestingView(View):
#
#     def post(self,request,*args,**kwargs):
#         if request.is_ajax():
#             data = request.POST
#             return JsonResponse({"online":"true"})
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(AjaxRequestTestingView, self).dispatch(request, *args, **kwargs)

# Just a testing case
# class TestingView(View):
#     http_method_names = ['get', 'post']
#     template_name = 'development/base/index.html'
#
#     def get(self, request, *args, **kwargs):
#         print([m.upper() for m in self.http_method_names if hasattr(self, m)])
#         response = render(request, self.template_name, {})
#         response.cookies['munis'] = True
#         response._headers['Developer'] = ('Developer','Munis Isazade')
#         return render(request, self.template_name, {})


#####################################################################
################## Latest Footer Contact Form #######################
#####################################################################

class LeaveMessageView(TezsagalBaseView,
                       FormView):
    model = ContactMessages
    form_class = LeaveMessageForm


class Test(TezsagalBaseView, TemplateView):
    template_name = 'development/testing/index.html'


class PersonalInfoDoctorView(TezsagalBaseView,
                             FormView):
    template_name = 'production/base'


class DoctorFormsView(ListView):
    model = DoctorBlog
    queryset = DoctorBlog.objects.filter(status=True)
    template_name = 'production/forms/index.html'

    def get_nav_menu_contacts(self):
        obj = BaseContact.objects.all().last()
        return obj

    def get_context_data(self, **kwargs):
        context = super(DoctorFormsView, self).get_context_data(**kwargs)
        context['base_menu_contact'] = self.get_nav_menu_contacts()
        return context


class DoctorBlogDetailView(TezsagalBaseView,
                           DetailView):
    model = DoctorBlog
    template_name = 'production/blog/index.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorBlogDetailView, self).get_context_data(**kwargs)
        return context


class DoctorTvView(TezsagalBaseView,
                   ListView):
    model = BlogTv
    template_name = 'production/tv/index.html'


class SendMail(View):
    def get(self, request, **kwargs):
        email_template = 'email/register.html'
        subject, from_email, to = 'Emailinizi Təstiqləyin zəhmət olmasa', settings.EMAIL_HOST_USER, "munisisazade@gmail.com"
        text_content = 'This is an important message.'
        ctx = {
            'user_full_name': "Munis",
            'confirm_link': "asdasd"
        }
        message = get_template(email_template).render(ctx)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(message, "text/html")
        return HttpResponse("Mesaj gonderildi")

class DoctorBaseSearchView(BaseIndexView,TemplateView):
    template_name = 'production/search/index.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorBaseSearchView, self).get_context_data(**kwargs)
        context['illnes'] = []
        context['illne'] = self.request.GET.getlist('ilness')
        context['areas'] = []
        context['area'] = self.request.GET.getlist('area')
        context['money'] = self.request.GET.get('money', False)
        context['gender'] = self.request.GET.get('gender', False)
        context['goster'] = self.request.GET.get('gosterici', False)
        context['rating_f'] = self.request.GET.get('rating', False)
        context['loop_stars'] = range(1, 5)
        rating_f = Decimal(context['rating_f'])
        # return HttpResponse()
        # try:
        all = Doctor.objects.filter(payment_status=True, tesdiq=True).order_by('-rate').order_by('qebul_qiymeti')
        if context['money']:
            if context['money'] != '-1':
                all = all.filter(qebul_qiymeti__range=[int(context['money'].split("-")[0]),
                                                   int(context['money'].split("-")[1])])

        if context['gender']:
            if int(context['gender']) != 0:
                all = all.filter(user__gender=context['gender'])
        if context['rating_f']:
            # print('asas')
            all = all.filter(rate__gte=Decimal(rating_f)-Decimal(0.5)).filter(rate__lte=Decimal(rating_f)+Decimal(0.5))
                # .filter(rate__lte=rating_f-1)

        include_areas_doctors = []
        bool_area_tr = False
        if context['area']:
            for x in context['area']:
                if x:
                    bool_area_tr = True
                    break
            # print('bool_area_tr')
            if bool_area_tr:
                # print('bool_area_tr')
                context['areas'] = [int(x) for x in self.request.GET.getlist('area')]
                doctor_areas = DoctorCountry.objects.filter(country__id__in=context['area'])
                for doctor_area in doctor_areas:
                    include_areas_doctors.append(doctor_area.doctor.id)
                all = all.filter(id__in=include_areas_doctors)
        include_illnes_doctors = []
        bool_illne_tr = False
        if context['illne']:
            for x in context['illne']:
                if x:
                    bool_illne_tr = True
                    break
            # print('sdsd')
            if bool_illne_tr:
                context['illnes'] = [int(x) for x in self.request.GET.getlist('ilness')]
                doctor_illnes = DoctorXestelik.objects.filter(xestelik__id__in=context['illne'])
                for doctor_illne in doctor_illnes:
                    include_illnes_doctors.append(doctor_illne.doctor.id)
                print(all.count())
                all = all.filter(id__in=include_illnes_doctors)
                print(all.count())
        if context['rating_f'] == False and context['gender'] == False and context['gender'] == False and bool_illne_tr == False and bool_area_tr == False:
            print('all false')
            print(bool_area_tr)
            print(bool_illne_tr)
            print('all false')
            all = all.filter(id=0)

        search_obj = []

        for data in all:
            if data.get_country_list():
                for x in data.get_country_list():
                    for y in context['areas']:
                        if x.country.id == y:
                            search_obj.append(data)
                        else:
                            pass
        for obj in list(set(search_obj)):
            if obj.get_xestelik():
                for x in obj.get_xestelik():
                    try:
                        context['illnes'] = [int(x) for x in self.request.GET.getlist('ilness')]
                        for y in context['illnes']:
                            if x.xestelik.id == y:
                                search_obj.append(obj)
                            else:
                                pass
                    except:
                        pass
        context['data'] = all
        # except:
        #     print('ecept')
        #     context['data'] = False
        context['banner'] = Banner.objects.all()
        return context

class UploadFirstImage(View):
    def post(self, request, **kwargs):
        if request.is_ajax():
            image = request.FILES.get('')
            return JsonResponse({'upload': 'true'})


class ChangeProfilePicture(FormView):
    form_class = ChangePictureForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                object = get_object_or_404(User,id=request.user.id)
                object.profile_picture = form.cleaned_data['profile_image']
                object.save()
                return JsonResponse({"upload": "true"})
            else:
                return JsonResponse({"upload": "false"})
        else:
            return HttpResponse('not allowed')


class ChangeProfilePictureOne(FormView):
    form_class = ChangePictureForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                object = get_object_or_404(User,id=request.user.id)
                object.profile_picture_1 = form.cleaned_data['profile_image']
                object.save()
                return JsonResponse({"upload": "true"})
            else:
                return JsonResponse({"upload": "false"})
        else:
            return HttpResponse('not allowed')


class ChangeProfilePictureTwo(FormView):
    form_class = ChangePictureForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                object = get_object_or_404(User,id=request.user.id)
                object.profile_picture_2 = form.cleaned_data['profile_image']
                object.save()
                return JsonResponse({"upload": "true"})
            else:
                return JsonResponse({"upload": "false"})
        else:
            return HttpResponse('not allowed')


class DoctorDetailTestView(TezsagalBaseView, DetailView):
    model = User
    template_name = 'production/doctor/details.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorDetailTestView, self).get_context_data(**kwargs)


        context['object_base'] = get_object_or_404(Doctor,user_id=self.object.id)
        blogComments = BlogComment.objects.filter(doctor=context['object_base'])
        # v_star = 0
        # m_star = 0
        # for blogComment in blogComments:
        #     v_star += blogComment.star
        # if v_star == 0:
        #     v_star=5
        # else:
        #     if blogComments.count() == 0:
        #         m_star = 0
        #     else:
        #         m_star = v_star/blogComments.count()
        if not self.request.user.is_authenticated():
            show_review_form = False
        else:
            if MeetingModels.objects.filter(status=True):
                show_review_form = True
            else:
                show_review_form = False
        context['show_review_form'] = show_review_form
        context['review'] = blogComments
        context['loop_stars'] = range(1, 5)
        # context['m_star'] = m_star
        return context

class StaticPageView(TezsagalBaseView, TemplateView):
    model = StaticPage
    template_name = 'production/page/static-page.html'

    def get_context_data(self, **kwargs):
        context = super(StaticPageView, self).get_context_data(**kwargs)

        print(self.kwargs['slug'])
        context['v_static_page'] = get_object_or_404(StaticPage,url=self.kwargs['slug'])
        # context['m_star'] = m_star
        return context


class MeetDoctorTestView(LoginRestrictedMixin,TezsagalBaseView, TemplateView):
    template_name = 'production/meet_doctor/meet.html'

    def post(self, request, *args, **kwargs):
        doctors = get_object_or_404(Doctor,id=request.POST.get('doctor_id'))
        # d = DoctorTimeTable.objects.get(doctor=doctors,time=datetime.strptime(request.POST.get('date'),'%m/%d/%Y'))
        meet = MeetingModels(
            user=request.user,
            doctor=doctors,
            meet_time=datetime.strptime(request.POST.get('date'), '%m/%d/%Y'),
            tarix=datetime.strptime(request.POST.get('tarix'), '%H:%M'),
            text=request.POST.get('sebeb'),
            payment=int(request.POST.get('pay')),
            question=bool(int(request.POST.get('question')))
        )
        meet.save()
        if request.POST.get('pay') == '1':
            background_send = Thread(target=MeetingRequestToDoctor, args=(doctors, meet))
            background_send.start()
            return redirect(reverse("base:doctor-meeting-done") + "?doctor=" + str(doctors.id))
        else:
            return redirect(reverse("base:pay-user-meet") + "?money=" + str(doctors.qebul_qiymeti) + "00")

    def get_context_data(self, **kwargs):
        context = super(MeetDoctorTestView, self).get_context_data(**kwargs)
        if self.request.GET.get('doctor', False) and self.request.GET.get('user', False):
            context['doctor'] = get_object_or_404(Doctor,id=self.request.GET.get('doctor', False))
            context['pasient'] = get_object_or_404(User,id=self.request.user.id)
            context['now'] = datetime.now()
            context['pasient'] = get_object_or_404(User,id=self.request.user.id)
        return context


class DashboradEducation(TezsagalBaseView, TemplateView):
    template_name = 'production/dashboard/education.html'

    def post(self, request, *args, **kwargs):
        doctors = get_object_or_404(Doctor,user=request.user)
        if not doctors.step_2:
            doctors.education_az = request.POST.get('education_az')
            doctors.education_ru = request.POST.get('education_ru')
            doctors.education_ka = request.POST.get('education_ka')
            doctors.step_2 = True
            doctors.save()
            return redirect(reverse('base:dashboard-work'))
        else:
            doctors.education_az = request.POST.get('education_az')
            doctors.education_ru = request.POST.get('education_ru')
            doctors.education_ka = request.POST.get('education_ka')
            doctors.save()
            return redirect(reverse('base:dashboard-work'))

    def get_context_data(self, **kwargs):
        context = super(DashboradEducation, self).get_context_data(**kwargs)
        context['doctor'] = get_object_or_404(Doctor,user=self.request.user)
        return context


class DashboradWork(TezsagalBaseView, TemplateView):
    template_name = 'production/dashboard/work_experience.html'

    def post(self, request, *args, **kwargs):
        doctors = get_object_or_404(Doctor,user=request.user)
        if not doctors.step_3:
            doctors.job_description_az = request.POST.get('job_description_az')
            doctors.job_description_ru = request.POST.get('job_description_ru')
            doctors.job_description_ka = request.POST.get('job_description_ka')
            doctors.step_3 = True
            doctors.save()
            return redirect(reverse('base:dashboard-activity'))
        else:
            doctors.job_description_az = request.POST.get('job_description_az')
            doctors.job_description_ru = request.POST.get('job_description_ru')
            doctors.job_description_ka = request.POST.get('job_description_ka')
            doctors.save()
            return redirect(reverse('base:dashboard-activity'))

    def get_context_data(self, **kwargs):
        context = super(DashboradWork, self).get_context_data(**kwargs)
        context['doctor'] = get_object_or_404(Doctor,user=self.request.user)
        return context


class DashboradNealiyyet(TezsagalBaseView, TemplateView):
    template_name = 'production/dashboard/activities.html'

    def post(self, request, *args, **kwargs):
        doctors = get_object_or_404(Doctor,user=request.user)
        if not doctors.step_4:
            doctors.goals_az = request.POST.get('goals_az')
            doctors.goals_ru = request.POST.get('goals_ru')
            doctors.goals_ka = request.POST.get('goals_ka')
            doctors.step_4 = True
            doctors.save()
            return redirect(reverse('base:dashboard-meet-date'))
        else:
            doctors.goals_az = request.POST.get('goals_az')
            doctors.goals_ru = request.POST.get('goals_ru')
            doctors.goals_ka = request.POST.get('goals_ka')
            doctors.save()
            return redirect(reverse('base:dashboard-meet-date'))

    def get_context_data(self, **kwargs):
        context = super(DashboradNealiyyet, self).get_context_data(**kwargs)
        context['doctor'] = get_object_or_404(Doctor,user=self.request.user)
        return context


class DashboardMeetDateView(TezsagalBaseView, TemplateView):
    template_name = 'production/dashboard/meet_date.html'

    def post(self, request, *args, **kwargs):
        doctors = get_object_or_404(Doctor,user=self.request.user)
        zaman = request.POST.get('date')
        doctor_country_payment = request.POST.get('doctor_country_payment',0)
        if zaman != '':
            for tarix in zaman.split(','):
                try:
                    tarix = tarix.replace(' ', '')
                    DoctorTimeTable.objects.get(time=datetime.strptime(tarix, '%m/%d/%Y'), doctor=doctors)
                    pass
                except:
                    tarix = tarix.replace(' ', '')
                    tar = DoctorTimeTable(
                        time=datetime.strptime(tarix, '%m/%d/%Y'),
                        doctor=doctors
                    )
                    tar.save()
        doctors.start_date = datetime.strptime(request.POST.get('start'), "%H:%M") if request.POST.get(
            'start') != '' else datetime.strptime('12:00', "%H:%M")
        doctors.end_date = datetime.strptime(request.POST.get('end'), "%H:%M") if request.POST.get(
            'end') != '' else datetime.strptime('23:00', "%H:%M")
        doctors.step_5 = True
        doctors.save()
        if doctors.payment_status:
            return redirect(reverse('base:dashboard-payment-success'))
        else:
            reverse_url = ''
            if doctors.work_country and doctor_country_payment:
                reverse_url = reverse('base:pay-doctor-register')+'?doctor_country_payment='+str(doctor_country_payment)
            else:
                raise Http404
            # return HttpResponse(reverse_url)
            return redirect(reverse_url)

    def get_context_data(self, **kwargs):
        context = super(DashboardMeetDateView, self).get_context_data(**kwargs)
        doctor = get_object_or_404(Doctor,user=self.request.user)
        if doctor.work_country:
            context['doctor_country_payments'] = PaymentWorkCountry.objects.filter(work_country=doctor.work_country)
        context['doctor'] = doctor
        return context


class DoctorRegisterPaymentSuccess(TezsagalBaseView, TemplateView):
    template_name = 'production/dashboard/register_payment.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorRegisterPaymentSuccess, self).get_context_data(**kwargs)
        context['doctor'] = get_object_or_404(Doctor,user=self.request.user)
        return context


class SposorMoneyView(TezsagalBaseView, TemplateView):
    template_name = 'production/dashboard/sponsor.html'

    def post(self, request, *args, **kwargs):
        doctors = get_object_or_404(Doctor,user=request.user)
        sponsored = SponsorModel(
            doctor=doctors,
            place=request.POST.get('place'),
            prize=int(request.POST.get('money')) / 100,
        )
        sponsored.save()
        return redirect(reverse('base:pay-doctor-sponsored') + "?money=" + str(request.POST.get('money', 0)))


class DoctorAddBlog(TezsagalBaseView, FormView):
    form_class = BlogAddForm
    template_name = 'production/dashboard/add_blog.html'
    success_url = "/az/account/success/"

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Adminin təstiqindən sonra blogunuz saytda paylaşılacaq. Təşəkkürlər"

        )
        return super(DoctorAddBlog, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponse("Error")

    def get_context_data(self, **kwargs):
        context = super(DoctorAddBlog, self).get_context_data(**kwargs)
        context['doctor'] = get_object_or_404(Doctor,user=self.request.user)
        return context


class DoctorBlogList(TezsagalBaseView, TemplateView):
    template_name = 'production/dashboard/my_blogs.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorBlogList, self).get_context_data(**kwargs)
        doctor = get_object_or_404(Doctor,user=self.request.user)
        context['doctor_blogs'] = DoctorBlog.objects.filter(author=doctor)
        return context


class MeetingDoneView(TezsagalBaseView, TemplateView):
    template_name = 'production/meet_doctor/meet_done.html'

    def get_context_data(self, **kwargs):
        context = super(MeetingDoneView, self).get_context_data(**kwargs)
        if self.request.GET.get('doctor'):
            context['doctor'] = Doctor.objects.get(id=self.request.GET.get('doctor'))
        return context


class PasiendListView(TezsagalBaseView, TemplateView):
    template_name = 'production/dashboard/pasient_list.html'

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        doctor = get_object_or_404(Doctor,user=request.user)
        obj = MeetingModels.objects.filter(doctor=doctor, user=user).last()
        obj.status = True
        obj.save()
        url = "https://tezsagal.az/az/dashboard/add_review/?user=%s&doctor=%s" % (user.id, doctor.id)
        background_send = Thread(target=ReviewMessages, args=(doctor, user, url))
        background_send.start()
        return redirect(reverse("base:dashboard-pasient"))

    def get_context_data(self, **kwargs):
        context = super(PasiendListView, self).get_context_data(**kwargs)
        doctor = get_object_or_404(Doctor,user=self.request.user)
        context['data'] = MeetingModels.objects.filter(doctor=doctor).exclude(is_accept='reject').order_by('-id')
        return context


class AddReview(TezsagalBaseView, TemplateView):
    template_name = 'production/meet_doctor/add_review.html'

    # @login_required(login_url='login')
    def get_context_data(self, **kwargs):
        context = super(AddReview, self).get_context_data(**kwargs)
        if self.request.GET.get('doctor', False):
            doctor_o = get_object_or_404(Doctor,id=int(self.request.GET.get('doctor', False)))
            context['doctor'] = doctor_o
            return_url = reverse('base:doctor-detail', kwargs={'slug': doctor_o.user.slug})
            if not self.request.user.is_authenticated():
                show_review_form = False
                return HttpResponseRedirect(return_url)
            else:
                meetings = MeetingModels.objects.filter(status=True,user=self.request.user,doctor=doctor_o)
                comments = BlogComment.objects.filter(user=self.request.user,doctor=doctor_o)
                if meetings.count() >= comments.count() and meetings.count() > 0:
                    show_review_form = True
                else:
                    show_review_form = False
                    return HttpResponseRedirect(return_url)
            context['show_review_form'] = show_review_form
            # print('aaaa')
            context['pasient'] = User.objects.get(id=self.request.user.id)
        return context


@login_required(login_url='login')
def doctor_comment_ajax(request, id):
    # message_code = 0
    # message = ''
    return_url = ' '
    content = ''
    if request.method == 'POST' and request.is_ajax():
        t_message = request.POST.get('message')
        t_rating = request.POST.get('star')
        t_prepare_paying_process = request.POST.get('star-prepare_paying_process')
        t_office_status = request.POST.get('star-office_status')
        t_registration_status = request.POST.get('star-registration_status')
        t_follow_after_examination = request.POST.get('star-follow_after_examination')
        t_diagnosis = request.POST.get('star-diagnosis')
        t_working_politeness = request.POST.get('star-working_politeness')
        t_spend_time = request.POST.get('star-spend_time')
        user = request.user
        doctor_o = Doctor.objects.filter(id=id).first()
        if MeetingModels.objects.filter(user=user,doctor=doctor_o):
            if (doctor_o) and type(int(t_rating)) == int:
                try:
                    star_s = ''
                    for i in range(1, int(t_rating), 1):
                        star_s += '★'
                    blog_comment_o = BlogComment(
                        user=user,
                        doctor=doctor_o,
                        star=t_rating,
                        diagnosis=t_diagnosis,
                        spend_time=t_spend_time,
                        follow_after_examination=t_follow_after_examination,
                        registration_status=t_registration_status,
                        working_politeness=t_working_politeness,
                        office_status=t_office_status,
                        prepare_paying_process=t_prepare_paying_process,
                        text=t_message
                    )
                    blog_comment_o.save()
                    blogComments = BlogComment.objects.filter(doctor=doctor_o)
                    g_star = 0
                    g_diagnosis = 0
                    g_spend_time = 0
                    g_follow_after_examination = 0
                    g_registration_status = 0
                    g_working_politeness = 0
                    g_office_status = 0
                    g_prepare_paying_process = 0
                    for blogComment in blogComments:
                        g_star += int(blogComment.star)
                        g_diagnosis += int(blogComment.diagnosis)
                        g_spend_time += int(blogComment.spend_time)
                        g_follow_after_examination += int(blogComment.follow_after_examination)
                        g_registration_status += int(blogComment.registration_status)
                        g_working_politeness += int(blogComment.working_politeness)
                        g_office_status += int(blogComment.office_status)
                        g_prepare_paying_process += int(blogComment.prepare_paying_process)
                    # if v_star == 0:
                    #     v_star = 5
                    # else:
                    if blogComments.count() <= 0:
                        m_star = 0
                        m_diagnosis = 0
                        m_spend_time = 0
                        m_follow_after_examination = 0
                        m_registration_status= 0
                        m_working_politeness = 0
                        m_office_status = 0
                        m_prepare_paying_process = 0
                    else:
                        m_star = g_star / blogComments.count()
                        m_diagnosis = g_diagnosis / blogComments.count()
                        m_spend_time = g_spend_time / blogComments.count()
                        m_follow_after_examination = g_follow_after_examination / blogComments.count()
                        m_registration_status= g_registration_status / blogComments.count()
                        m_working_politeness = g_working_politeness / blogComments.count()
                        m_office_status = g_office_status / blogComments.count()
                        m_prepare_paying_process = g_prepare_paying_process / blogComments.count()
                    doctor_o.rate_general_rate = round(m_star, 5)
                    doctor_o.rate_spend_time = round(m_spend_time, 5)
                    doctor_o.rate_working_politeness = round(m_working_politeness, 5)
                    doctor_o.rate_diagnosis = round(m_diagnosis, 5)
                    doctor_o.rate_follow_after_examination = round(m_follow_after_examination, 5)
                    doctor_o.rate_registration_status = round(m_registration_status, 5)
                    doctor_o.rate_office_status = round(m_office_status, 5)
                    doctor_o.rate_prepare_paying_process = round(m_prepare_paying_process, 5)
                    if blogComments.count() <= 0:
                        doctor_o.rate = 0
                    else:
                        v_rate = (m_star + m_spend_time + m_working_politeness + m_diagnosis + m_follow_after_examination + m_registration_status + m_office_status + m_prepare_paying_process) / 8
                        doctor_o.rate = round(v_rate,5)
                    doctor_o.save()
                    return_url = reverse('base:doctor-detail', kwargs={'slug': doctor_o.user.slug})
                    message_code = 1
                    message = _('Rəyiniz Uğurla Qeyd alındı')
                    content = '{0}{1}'.format(content, render_to_string(
                        'production/doctor/_include/_comment_part.html',
                        {
                            'x': blog_comment_o,
                            'star_s': star_s,
                        }))
                except:
                    message_code = 0
                    message = _('Xaiş edirik təkrar cəhd edin')
            else:
                message_code = 0
                message = _('Xaiş edirik təkrar cəhd edin')
        else:
            message_code = 0
            message = _('Həkimin Qəbulunda olmadan Rəy yaza bilməzsiziniz')
        data = {"message": message, 'message_code': message_code,'return_url':return_url,'content':content}
        return JsonResponse(data)

    else:
        raise Http404

@login_required(login_url='login')
def doctor_meeting_accept(request, m_id,a_slug):
    user = request.user
    # return HttpResponse('sasas')
    doctor_o = get_object_or_404(Doctor,user=user)
    meeting_o = get_object_or_404(MeetingModels,id=m_id,doctor=doctor_o)
    return_url = reverse('base:dashboard-pasient')
    if meeting_o.status == False and meeting_o.is_accept == 'waiting':
        # return HttpResponse('sasas')
        meet = meeting_o
        if a_slug=='accept':
            meeting_o.is_accept = 'accept'
            background_send = Thread(target=MeetingResponseToPasient(meet))
            background_send.run()
        elif a_slug=='reject':
            meeting_o.is_accept = 'reject'
        else:
            return HttpResponseRedirect(return_url)
        meeting_o.save()
        return HttpResponseRedirect(return_url)
    else:
        # return HttpResponse('else')
        return HttpResponseRedirect(return_url)
