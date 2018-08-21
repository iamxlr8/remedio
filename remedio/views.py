from django.shortcuts import render
from django.http import HttpResponse
from remedio.forms import logform,signform

# Create your views here.
def hello(request):
	return HttpResponse("HELLO!! Go to /remedio/ for further processes.")


def index(request):
    form1=logform()
    form2=signform()
    return render(request,'remedio/remedio.html',{'form1':form1,'form2':form2})

def loggedin(request):
    if request.method=='POST':
        form1=logform(request.POST)
        if form1.is_valid():
            uname=form1.cleaned_data['u_name']
            passwd=form1.cleaned_data['passwd']
            return render(request,'remedio/loggedin.html',{'uname':uname,'passwd':passwd})

def signedup(request):
    if request.method=='POST':
        form2=signform(request.POST)
        if form2.is_valid():
            fname=form1.cleaned_data['first_name']
            lname=form1.cleaned_data['last_name']
            return render(request,'remedio/signedup.html',{'fname':fname,'lname':lname})
