from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
import os
from django import forms


def getFile(request,filename):
    nowtime = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    newFileName = "%s%s"%(nowtime,filename)
    return os.path.join('images/',newFileName)

class particpants(models.Model):
    username = models.CharField(max_length=100,null=False, blank=False)
    password = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to=getFile,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.username


class tender(models.Model):
    title = models.CharField(max_length=100,null=False, blank=False)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    img = models.ImageField(upload_to=getFile,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    tenderNo = models.CharField(max_length=100,null=False,blank=False)
    status=  models.BooleanField(default=True)
    winnerid=  models.IntegerField(default=0)
    initalCotation = models.CharField(max_length=100,null=False,blank=False,default=0)
    

class particpantForm(forms.ModelForm):
    class Meta:
        model = particpants
        fields = ['username','password','contact','email']
        widgets ={
           'username': forms.TextInput(attrs={'type': 'text', 'placeholder':'Enter Username', 'class': 'form-control'}),
           'password': forms.TextInput(attrs={'type': 'password' , 'placeholder':'Enter password', 'class': 'form-control'}),
           'contact': forms.TextInput(attrs={'type': 'number', 'placeholder':'Enter Contact Number', 'class': 'form-control'}),
           'email': forms.EmailInput(attrs={'type': 'email', 'placeholder':'Enter Email Address', 'class': 'form-control'}),
        }

class TenderForm(forms.ModelForm):
    class Meta:
        model=tender
        fields=['title','started_at','ended_at','tenderNo','img','initalCotation' ]
        widgets = {
           'started_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
           'ended_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),

        }


class LoginParticpantForm(forms.ModelForm):
    class Meta:
        model = particpants
        fields = ['email','password']
        widgets ={
           'email': forms.EmailInput(attrs={'type': 'email', 'placeholder':'Enter Email Address', 'class': 'form-control'}),
           'password': forms.TextInput(attrs={'type': 'password' , 'placeholder':'Enter password', 'class': 'form-control'}),
        }


def default_data():
    """
    Default value for the data field.
    """
    return {'updated_at': timezone.now().isoformat()} 

#Blockchain table
class Blockchain(models.Model):
    tenderid= models.CharField(max_length=100,null=False, blank=False)
    previousHash = models.CharField(max_length=100,null=False, blank=False)
    currentHash = models.CharField(max_length=100,null=False, blank=False)
    data = models.JSONField(default=default_data) 
    updated_at=models.DateTimeField(auto_now_add=True)


class tenderCotated(models.Model):
    tenderid= models.CharField(max_length=100,null=False, blank=False)
    userid = models.CharField(max_length=100,null=False, blank=False)
    updated_at=models.DateTimeField(auto_now_add=True)
