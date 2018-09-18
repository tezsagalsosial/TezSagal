from django.conf.urls import url
from doctor.paymen_views import DoctorRegisterPayment, SponsorPayment, UserMeetPayment
from doctor.views import BaseIndexView, DashboardView, Test, DoctorFormsView, \
    DoctorBlogDetailView, DoctorTvView, SendMail, DoctorBaseSearchView, \
    ChangeProfilePicture,  MeetDoctorTestView, DashboradEducation, \
    DashboradWork, DashboradNealiyyet, ChangeProfilePictureOne, ChangeProfilePictureTwo, \
    DashboardMeetDateView, DoctorRegisterPaymentSuccess, DoctorDetailTestView, \
    SposorMoneyView, DoctorAddBlog, DoctorBlogList, MeetingDoneView, PasiendListView, \
    AddReview,StaticPageView
from .views import doctor_comment_ajax, doctor_meeting_accept

urlpatterns = [
    url(r'^$', BaseIndexView.as_view(), name="index"),
    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
    # url(r'^', include("news.urls")),
    # base settings page
    url(r'^dashboard/education/$', DashboradEducation.as_view(), name="dashboard-education"),
    url(r'^dashboard/work_experience/$', DashboradWork.as_view(), name="dashboard-work"),
    url(r'^dashboard/activities/$', DashboradNealiyyet.as_view(), name="dashboard-activity"),
    url(r'^dashboard/personal-info/$', DashboardView.as_view(), name="dashboard-personal"),
    url(r'^dashboard/meet-date/$', DashboardMeetDateView.as_view(), name="dashboard-meet-date"),
    url(r'^dashboard/payment/$', DoctorRegisterPaymentSuccess.as_view(), name="dashboard-payment-success"),
    url(r'^dashboard/sponsored/$', SposorMoneyView.as_view(), name="dashboard-sponsor"),
    url(r'^dashboard/pasients/$', PasiendListView.as_view(), name="dashboard-pasient"),
    url(r'^dashboard/pasient/accept/(?P<m_id>[0-9]+)/(?P<a_slug>[-\w]+)/$', doctor_meeting_accept, name="doctor_meeting_accept"),
    url(r'^dashboard/add_review/$', AddReview.as_view(), name="add-review"),

    url(r'^testing/$', Test.as_view(), name="test"),
    url(r'^forms/$', DoctorFormsView.as_view(), name="doctor-blog"),
    url(r'^ajax/comment-ajax/(?P<id>[-\w]+)/dsdsds/$', doctor_comment_ajax, name="doctor_comment_ajax"),
    url(r'^tv/$', DoctorTvView.as_view(), name="doctor-tv"),
    url(r'^blog/(?P<slug>[-\w]+)/$', DoctorBlogDetailView.as_view(), name="doctor-blog"),
    url(r'^sendmail/$', SendMail.as_view(), name="send-mail"),
    url(r'^search/$', DoctorBaseSearchView.as_view(), name="search"),
    url(r'^doctor/(?P<slug>[-\w]+)/$', DoctorDetailTestView.as_view(), name="doctor-detail"),
    url(r'^page/(?P<slug>[\w-]+)/$', StaticPageView.as_view(), name="custom-page"),
    url(r'^doctor/add/blog/$', DoctorAddBlog.as_view(), name="doctor-add-blog"),
    url(r'^doctor/list/blog/$', DoctorBlogList.as_view(), name="doctor-blog-list"),
    url(r'^meet/doctor/$', MeetDoctorTestView.as_view(), name="doctor-meet"),
    url(r'^meet/done/$', MeetingDoneView.as_view(), name="doctor-meeting-done"),
    url(r'^picture/upload/$', ChangeProfilePicture.as_view(), name="upload-picture"),
    url(r'^picture/upload/one/$', ChangeProfilePictureOne.as_view(), name="upload-picture1"),
    url(r'^picture/upload/two/$', ChangeProfilePictureTwo.as_view(), name="upload-picture2"),


    # Odenishlerin url tehlukesiz
    url(r'^user/meeting/payment/$', UserMeetPayment.as_view(), name="pay-user-meet"),
    url(r'^doctor/registration/payment/$', DoctorRegisterPayment.as_view(), name="pay-doctor-register"),
    url(r'^doctor/sponsored/payment/$', SponsorPayment.as_view(), name="pay-doctor-sponsored"),

]