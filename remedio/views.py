from django.shortcuts import render
from django.http import HttpResponse
from . import forms

# Create your views here.
def hello(request):
	return HttpResponse("HELLO!! Go to /remedio/ for further processes.")


def index(request):
	return render(request,'remedio/remedio.html')