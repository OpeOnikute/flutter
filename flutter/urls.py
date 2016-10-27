from django.conf.urls import url
from . import views

app_name = 'flutter'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^results/', views.results, name='results'),

	]