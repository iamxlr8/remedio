from django.urls import path
from django.conf.urls import url
from remedio import views
from remedio.feeds import DreamrealCommentsFeed
app_name='remedio'

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^index/$',views.index,name='index'),
	url(r'^loggedin/',views.loggedin,name='loggedin'),
	url(r'^signedup/',views.signedup,name='signeup'),
	url(r'^symtest/',views.symtest,name='symtest'),
	url(r'^medication/',views.medication,name='medication'),
	url(r'^home/',views.home,name='home'),
	url(r'^prevpres/',views.prevpres,name='prevpres'),
	url(r'^loggedout/',views.loggedout,name='loggedout'),
    url(r'^feed/', DreamrealCommentsFeed()),
    url(r'^rate/', views.rate, name='rate'),
	url(r'^rating/', views.rating, name='rating')
]
