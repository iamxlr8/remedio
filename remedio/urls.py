from django.urls import path
from remedio import views

urlpatterns = [
	path('',views.index,name='index'),
]