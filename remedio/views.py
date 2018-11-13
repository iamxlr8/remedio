from django.shortcuts import render,redirect
from django.http import HttpResponse
from remedio.forms import *
from django.contrib.auth import *
from remedio.models import *
from functools import reduce
import operator
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import connection
from datetime import datetime
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('/loggedin/')
    if request.method == 'POST':
        username = request.POST.get('u_name')
        password = request.POST.get('passwd')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('/home/')
            else:
                return HttpResponse("Your Remedio account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        form1=logform()
        form2=signform()
        form3=signform2()
        return render(request,'remedio/remedio.html',{'form1':form1,'form2':form2,'form3':form3})

@login_required(login_url="/index/")
def home(request):
	return render(request,'remedio/home.html')

@login_required(login_url="/index/")
def prevpres(request):
	info=Presc.objects.filter(uid=request.user.id)
	date,medicine,disease=[],[],[]
	for i in info:
		date.append(i.date)
		dis1=Dis.objects.get(disid=i.disid)
		med1=Sympdis.objects.get(disid=i.disid)
		disease.append(dis1.disease)
		medicine.append(med1.medicine)
		print(request.user.first_name)
	return render(request,'remedio/prevpres.html',{'fname':request.user.first_name,'lname':request.user.last_name,'zip':zip(date,disease,medicine)})

@login_required(login_url="/index/")
def loggedout(request):
    logout(request)
    return redirect('/home/')

@login_required(login_url="/index/")
def loggedin(request):
    symfor=symform()
    return render(request,'remedio/loggedin.html',{'symform':symfor})

def signedup(request):
    if request.method=='POST':
        form2=signform(data=request.POST)
        form3=signform2(data=request.POST)
        if form2.is_valid() and form3.is_valid():
            user = form2.save()
            user.set_password(user.password)
            user.save()
            profile = form3.save(commit=False)
            profile.user = user
            profile.save()
        else:
            print(form2.errors, form3.errors)
    form11 = logform()
    form12 = signform()
    form13 = signform2()
    return render(request,'remedio/remedio.html',{'form1':form11,'form2':form12,'form3':form13})

n=0
diss=[]

@login_required(login_url="/index/")
def symtest(request):
	global n
	global diss
	if request.method=='POST':
        # global n
        # global diss
		n=int(request.POST.get('number'))
		symptoms=[]
		for i in range(1,n+1):
			symptoms.append(request.POST.get('sym'+str(i)))
		n=str(n)
		query = reduce(operator.or_, (Q(symptom=item) for item in symptoms))
		symids = Symp.objects.filter(query)
		diss=[[] for _ in range(len(symids))]
		i=-1
		for id in symids:
			i+=1
			for dis in Relate.objects.filter(symid=id.symid):
				diss[i].append(dis.disid)
		disease=Relate.objects.all()
		for i in diss:
			query = reduce(operator.or_, (Q(disid=item) for item in i))
			disease=disease.filter(query)
		diss=[]
		for i in disease:
			x=int(i.disid.disid)
			if x not in diss:
				diss.append(int(x))
		page = request.GET.get('page', 1)

		paginator = Paginator(diss, 1)
		try:
			disses = paginator.page(page)
		except PageNotAnInteger:
			disses = paginator.page(1)
		except EmptyPage:
			disses = paginator.page(paginator.num_pages)
		print(type(disses))
		for i in disses:
			n1 = str(i)
			with connection.cursor() as cursor:
				cursor.execute("SELECT symptom FROM symp WHERE symid IN (SELECT symid FROM relate WHERE disid= %s )",[str(i)])
				symp=cursor.fetchall()
			return render(request,'remedio/symtest.html',{'n':n1,'l':symp,'buses':disses})
	else:
        # global n
        # global diss
		if n == 0:
			return HttpResponse("Please enter the symptoms")
		page = request.GET.get('page', 1)

		paginator = Paginator(diss, 1)
		try:
			disses = paginator.page(page)
		except PageNotAnInteger:
			disses = paginator.page(1)
		except EmptyPage:
			disses = paginator.page(paginator.num_pages)
		print(type(disses))
		for i in disses:
			n1 = str(i)
			with connection.cursor() as cursor:
				cursor.execute("SELECT symptom FROM symp WHERE symid IN (SELECT symid FROM relate WHERE disid= %s )",
                               [str(i)])
				symp = cursor.fetchall()
			return render(request, 'remedio/symtest.html', {'n': n1, 'l': symp, 'buses': disses})

@login_required(login_url="/index/")
def medication(request):
    if request.method=="POST":
        disid=str(request.POST.get('disease'))
        # return HttpResponse(disid)
        #disid=int(disid)
        with connection.cursor() as cursor:
            cursor.execute("SELECT disease FROM dis WHERE disid = %s ",[disid])
            dis1 = cursor.fetchall()
            cursor.execute("SELECT medicine FROM sympdis WHERE disid = %s",[disid])
            med1 =cursor.fetchall()
            print(request.user.username)
            cursor.execute("INSERT into presc(uid,disid,date) values(%s,%s,%s) ",[str(request.user.id),disid,str(datetime.now().date())])
        return render(request, 'remedio/medication.html', {'n':disid, 'l':dis1 , 'p':med1})
