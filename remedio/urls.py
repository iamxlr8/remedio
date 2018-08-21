from django.urls import path
from remedio import views

urlpatterns = [
	path('',views.index,name='index'),
	path('remedio/loggedin/',views.loggedin,name='loggedin'),
	path('remedio/signedup/',views.signedup,name='signeup')
]