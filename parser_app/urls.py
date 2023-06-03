from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('homepage', views.homepage, name='homepage'),
    path('signuppage', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login_page', views.login_page, name='login_page'),
    path('check_status', views.check_status, name='check_status'),
    re_path(r'^logout$', views.logout, name='logout'),
    re_path(r'^adminlogout$', views.adminlogout, name='adminlogout'),
    path('home', views.home, name='home'),
    path('pyresults', views.pyresults, name='pyresults'),
    path('trresults', views.trresults, name='trresults'),
    path('hrresults', views.hrresults, name='hrresults'),
    path('jvresults', views.jvresults, name='jvresults'),
    path('teresults', views.teresults, name='teresults'),
    path('manresults', views.manresults, name='manresults'),
    re_path(r'^new/(?P<id>\d+)/$', views.new, name='new'),
    path('login', views.login, name='login'),
    path('mainhome', views.mainhome, name='mainhome'),
    path('', views.mainhome, name='mainhome'),
    path('aboutus', views.aboutus, name='aboutus'),
    re_path(r'^apply/(?P<id>\d+)/$', views.apply, name='apply'),
    path('availablejobs', views.availablejobs, name='availablejobs'),
    path('apply', views.apply, name='apply'),
    path('gallery', views.gallery, name='gallery'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('addjob', views.addjob, name='addjob'),
    path('adminhome', views.adminhome, name='adminhome'),
    path('viewapplicants', views.viewapplicants, name='viewapplicants'),
    path('newjob', views.newjob, name='newjob'),
    path('adlogin_page', views.adlogin_page, name='adlogin_page'),
    path('adminlogin', views.adminlogin, name='adminlogin'),
    path('adminPage', views.adminPage, name='adminPage'),
    path('viewjobs', views.viewjobs, name='viewjobs'),
    path('contactComment', views.writeComment, name='contactComment'),
    path('recruiterlogin', views.recruiterlogin, name='recruiterlogin'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
