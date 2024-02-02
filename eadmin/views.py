from django.shortcuts import render,redirect
from .models import particpantForm,LoginParticpantForm,particpants,tender
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
    participant_info = getattr(request, 'participant_info', None)
    if not participant_info:
        return redirect('login')  # Redirect to login if participant_info is not available
    logger.warning(str(participant_info.id))  # Log participant ID
    tenders = getattr(request, 'tenderList', None)
    logger.warning(f"Tenders: {tenders}") 
    
    return render(request, "e-participant/index.html", {'participant_info': participant_info,'tenders':tenders},)

    
def bid_details(request):
    participant_info = getattr(request, 'participant_info', None)
    if not participant_info:
        return redirect('login')  # Redirect to login if participant_info is not available
    return render(request, "e-participant/bid_details.html", {'participant_info': participant_info})

def getBidDetails(request,tender_id):
    tenders=tender.objects.get(pk=tender_id)
    logger.warning(f"tender:{tenders}")
    return render(request,'e-participant/tenderDetails.html',{'tenderDetails':tenders})
