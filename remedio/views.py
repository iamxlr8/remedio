from django.shortcuts import render
from . import forms

# Create your views here.
def index(request):
	return render(request,'remedio/remedio.html')