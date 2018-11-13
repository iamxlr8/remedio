from django.contrib import admin

# Register your models here.
from remedio.models import Dis,Relate,Sympdis,Symp,UserProfile,Presc
admin.site.register(Dis)
admin.site.register(Presc)
admin.site.register(Relate)
admin.site.register(Sympdis)
admin.site.register(Symp)
admin.site.register(UserProfile)
