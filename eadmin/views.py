from django.shortcuts import render,redirect
from .models import particpantForm,LoginParticpantForm,particpants
import datetime
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
def index(request):
    return render(request,"common/index.html")

def login(request):
    if request.method == 'POST':
        
        form = LoginParticpantForm(data= request.POST)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        logger.warning('login page was accessed at '+str(datetime.datetime.now())+' hours!'+email+','+password)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            particpant = particpants.objects.get(email=email)
            if particpant.password==password:
                print('success')
                return redirect('index') 
    else:
        form = LoginParticpantForm()
    return render(request,"common/loginPage.html", {'form':form})

def register(request):
    if request.method == 'POST':
        form = particpantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = particpantForm()
    return render(request,"common/registerPage.html",{'form':form})