from django.conf.urls import url,include

from Website.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/login/$', auth_views.login, name='login',),
    url(r'^accounts/logout/$', auth_views.logout,{'next_page': '/login/'}),
    url(r'^accounts/passwordreset/', auth_views.password_reset, name='passreset'),
    url(r'^accounts/signup/$', signup),
    url('^', include('django.contrib.auth.urls')),
    url(r'^[H|h]ome', Home, name='home'),
    url(r'^[A|a]+bout', About,name='about'),
    url(r'^[A|a]+nalytics',analytics,name='analytics'),
    #url(r'content.pdf',myPdf.as_view()),
    url(r'content.pdf',GeneratePdf.as_view())
    
    
]
