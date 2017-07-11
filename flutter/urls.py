from django.conf.urls import url
from . import views

app_name = 'flutter'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/', views.results, name='results'),
    url(r'^resend_OTP/', views.resend_OTP, name='resend_otp'),
    url(r'^enter_OTP/', views.enter_OTP, name='enter_otp'),
]
