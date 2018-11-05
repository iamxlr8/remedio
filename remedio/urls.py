from django.urls import path
from django.conf.urls import url
from remedio import views

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^index/$',views.index,name='index'),
	url(r'^loggedin/',views.loggedin,name='loggedin'),
	url(r'^signedup/',views.signedup,name='signeup'),
	url(r'^symtest/',views.symtest,name='symtest'),
	url(r'^medication/',views.medication,name='medication'),
]
