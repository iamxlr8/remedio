from django import forms
class logform (forms.Form):
    u_name=forms.CharField(required='true',label='',label_suffix='',widget=forms.TextInput(attrs={'name':'u_name','placeholder':'Username'}))
    passwd = forms.CharField(required='true',label='', label_suffix='', widget=forms.PasswordInput(attrs={'name': 'passwd', 'placeholder': 'Password'}))

class signform (forms.Form):
    first_name = forms.CharField(required='true',label='', label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required='true',label='', label_suffix='', widget=forms.TextInput(attrs={'placeholder': 'Last Name', }))
    username = forms.CharField(required='true',label='', label_suffix='', widget=forms.TextInput(attrs={'name': '', 'placeholder': 'Username'}))
    email = forms.EmailField(required='true',label='', label_suffix='', widget=forms.EmailInput(attrs={'name': '', 'placeholder': 'Email'}))
    password = forms.CharField(required='true',label='', label_suffix='', widget=forms.PasswordInput(attrs={'name': 'u_name', 'placeholder': 'Password'}))
    sex=forms.ChoiceField(required='true',choices=[('male','Male'),('female','Female')],label='',label_suffix='',widget=forms.RadioSelect())
    dob=forms.DateField(required='true',widget=forms.DateInput(attrs={'min':'0001-01-01','max':'9999-12-31','type':'date'}))