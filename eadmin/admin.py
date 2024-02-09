from django.contrib import admin
from .models import particpants
from .models import tender
class ParticipantList(admin.ModelAdmin):
    list_display = ('profile_picture','username','contact','email','created_at')

class tenderList(admin.ModelAdmin):
    list_display = ('img','title','started_at','ended_at','created_at','initalCotation')

# Register your models here.
admin.site.register(particpants,ParticipantList)
admin.site.register(tender,tenderList)