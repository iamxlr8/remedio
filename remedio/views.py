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
        return redirect('/loggedin/')			# redirecting the user to the logged in page if authenticated
    if request.method == 'POST':				# else login
        username = request.POST.get('u_name')
        password = request.POST.get('passwd')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('/home/')		# redirecting the user to home page if no errors
            else:
                return HttpResponse("Your Remedio account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        form1=logform()							# registering the user
        form2=signform()
        form3=signform2()
        return render(request,'remedio/remedio.html',{'form1':form1,'form2':form2,'form3':form3})

@login_required(login_url="/index/")
def home(request):
	return render(request,'remedio/home.html',{'a':request.user.username})

@login_required(login_url="/index/")
def prevpres(request):							# view for showing previous prescriptions of the user
	info=Presc.objects.filter(uid=request.user.id)
	date,medicine,disease=[],[],[]
	for i in info:								# collecting date, disease and medicine recommended
		date.append(i.date)
		dis1=Dis.objects.get(disid=i.disid)
		med1=Sympdis.objects.get(id=i.disid)
		disease.append(dis1.disease)
		medicine.append(med1.medicine)
		print(request.user.first_name)
	if disease==[]:
		error=True
	else:
		error=False
	return render(request,'remedio/prevpres.html',{'fname':request.user.first_name,'lname':request.user.last_name,'zip':zip(date,disease,medicine),'a':request.user.username,'error':error})

@login_required(login_url="/index/")
def loggedout(request):							# log out
    logout(request)
    return redirect('/home/')

@login_required(login_url="/index/")
def loggedin(request):
    symfor=symform()
    return render(request,'remedio/loggedin.html',{'symform':symfor,'a':request.user.username})

def signedup(request):
    if request.method=='POST':					# view for sign up
        form2=signform(data=request.POST)
        form3=signform2(data=request.POST)		# collecting entered data and saving it in the user profile
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
def symtest(request):								# view for collecting the symptoms.
	global n
	global diss
	if request.method=='POST':
        # global n
        # global diss
		n=int(request.POST.get('number'))
		symptoms=[]
		for i in range(1,n+1):
			symptoms.append(request.POST.get('sym'+str(i)))			# collecting the symptoms entered
		n=str(n)
		query = reduce(operator.or_, (Q(symptom=item) for item in symptoms))		# construct query
		symids = Symp.objects.filter(query)							# collecting symptoms relative to query
		diss=[[] for _ in range(len(symids))]
		i=-1
		for id in symids:
			i+=1
			for dis in Relate.objects.filter(symid=id.symid):		# collecting all tuples relative to the particular symid
				diss[i].append(dis.disid)							# collecting the all the ids of diseases of particular symptom
		disease=Relate.objects.all()
		for i in diss:
			query = reduce(operator.or_, (Q(disid=item) for item in i))
			disease=disease.filter(query)     # collecting the common diseases of all the symptoms provided
		diss=[]
		for i in disease:
			x=int(i.disid.disid)
			if x not in diss:
				diss.append(int(x))
		page = request.GET.get('page', 1)

		# paginating the symptoms of diseases obtained

		paginator = Paginator(diss, 1)
		try:
			disses = paginator.page(page)
		except PageNotAnInteger:
			disses = paginator.page(1)
		except EmptyPage:
			disses = paginator.page(paginator.num_pages)
		# print(type(disses))
		for i in disses:
			n1 = str(i)
			with connection.cursor() as cursor:
				cursor.execute("SELECT symptom FROM symp WHERE symid IN (SELECT symid FROM relate WHERE disid= %s )",[str(i)])
				symp=cursor.fetchall()    # getting all the symptoms of particular disease
			return render(request,'remedio/symtest.html',{'n':n1,'l':symp,'buses':disses,'a':request.user.username})
	else:   # for pages other than first page after form submission
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
			return render(request, 'remedio/symtest.html', {'n': n1, 'l': symp, 'buses': disses,'a':request.user.username})

@login_required(login_url="/index/")
def medication(request):								# recommending medicines
    if request.method=="POST":
        disid=str(request.POST.get('disease'))
        # return HttpResponse(disid)
        #disid=int(disid)
        with connection.cursor() as cursor:				# collecting disease and medicine data
            cursor.execute("SELECT disease FROM dis WHERE disid = %s ",[disid])
            dis1 = cursor.fetchall()
            cursor.execute("SELECT medicine FROM sympdis WHERE id = %s",[disid])
            med1 =cursor.fetchall()
            print(request.user.username)
			# insert data into prescriptions
            cursor.execute("INSERT into presc(uid,disid,date) values(%s,%s,%s) ",[str(request.user.id),disid,str(datetime.now().date())])
        return render(request, 'remedio/medication.html', {'n':disid, 'l':dis1 , 'p':med1,'a':request.user.username})

@login_required(login_url="/index/")
def rate(request,object_pk):	# rating
	myrate = Rating.objects.get(user=object_pk)
	text = '<strong>User :</strong> %s ' % myrate.user
	text += '<strong>Comment :</strong> %s ' % myrate.rating
	return HttpResponse(text)

@login_required(login_url="/index/")
def rating(request):			# saving the data in database
	if request.method=="POST":
		rating=str(request.POST.get('rating'))
		time=str(datetime.now())
		user=str(request.user.username)
		with connection.cursor() as cursor:
			cursor.execute("INSERT into rating(rating,user,time) values (%s,%s,%s)",[rating,user,time])
		return redirect('/home/')
	else:
		return render(request,'remedio/rating.html')