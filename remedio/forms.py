from django import forms
from remedio.models import *

# login form

class logform (forms.Form):
    u_name=forms.CharField(required=True,label='',label_suffix='',widget=forms.TextInput(attrs={'name':'u_name','placeholder':'Username'}))
    passwd = forms.CharField(required=True,label='', label_suffix='', widget=forms.PasswordInput(attrs={'name': 'passwd', 'placeholder': 'Password'}))

# sign up form 1 (auth_user)

class signform (forms.ModelForm):
    first_name = forms.CharField(required=True,label='', label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True,label='', label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'Last Name', }))
    username = forms.CharField(required=True,label='', label_suffix='', widget=forms.TextInput(attrs={'name': '', 'placeholder': 'Username'}))
    email = forms.EmailField(required=True,label='', label_suffix='', widget=forms.EmailInput(attrs={'name': '', 'placeholder': 'Email'}))
    password = forms.CharField(required=True,label='', label_suffix='', widget=forms.PasswordInput(attrs={'name': 'u_name', 'placeholder': 'Password'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name','last_name')

# sighn up from 2 (extending the user)

class signform2(forms.ModelForm):
    sex=forms.ChoiceField(required=True,choices=[('male','Male'),('female','Female')],label='',label_suffix='',widget=forms.RadioSelect())
    dob=forms.DateField(required=True,widget=forms.DateInput(attrs={'min':'0001-01-01','max':'9999-12-31','type':'date'}))
    class Meta:
        model = UserProfile
        fields = ('sex','dob')

# form for entering symptoms

class symform(forms.Form):
    sym1=forms.CharField(required=True,label='',label_suffix='',widget=forms.TextInput(attrs={'id':'sym1','placeholder':'Enter a Symptom','style':'visibility:visible'}))
    sym2 = forms.CharField(required=False,label='', label_suffix='',widget=forms.TextInput(attrs={'id':'sym2','placeholder': 'Enter another Symptom', 'style': 'visibility:hidden'}))
    sym3 = forms.CharField(required=False,label='', label_suffix='',widget=forms.TextInput(attrs={'id':'sym3','placeholder': 'Enter another Symptom', 'style': 'visibility:hidden'}))
    sym4 = forms.CharField(required=False,label='', label_suffix='',widget=forms.TextInput(attrs={'id':'sym4','placeholder': 'Enter another Symptom', 'style': 'visibility:hidden'}))
    sym5 = forms.CharField(required=False,label='', label_suffix='',widget=forms.TextInput(attrs={'id':'sym5','placeholder': 'Enter another Symptom', 'style': 'visibility:hidden'}))
    number=forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'num','value':'1'}))