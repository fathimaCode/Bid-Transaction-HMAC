from django.shortcuts import render,redirect
from .models import particpantForm,LoginParticpantForm,particpants
import datetime
from django.contrib import messages
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
def index(request):
    return render(request,"common/index.html")

def login(request):
    if request.method == 'POST':
        form = LoginParticpantForm(data= request.POST)      
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            particpant = particpants.objects.get(email=email)
            if particpant.password==password:
                request.session['user_id']  = particpant.id  
                messages.success(request, 'Login successful!')
                return redirect('dashboard') 
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

def dashboard(request):
    user_id = request.session.get('user_id')
    participant_info = particpants.objects.get(pk=user_id)
    logger.warning(str(user_id))
    return render(request,"e-participant/index.html",{'participant_info': participant_info})
    
def bid_details(request):
    return render(request,"bid_details.html")