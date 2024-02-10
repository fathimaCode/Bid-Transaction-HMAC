from django.shortcuts import render,redirect
from .models import particpantForm,LoginParticpantForm,particpants,tender,Blockchain,tenderCotated
import datetime
from django.contrib import messages
from .HmacEncoderDecoder import HmacEncoderDecoder


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
    request.tender_id = tender_id
    block_list = getattr(request, 'block_list', None)
    participant_info = getattr(request, 'participant_info', None)
    return render(request,'e-participant/tenderDetails.html',{'tenderDetails':tenders,'block_list': block_list, 'participant_info': participant_info})


def newCotation(request):
    if request.method=='POST':
        cotedAmount = request.POST.get('amount')
        userId = request.POST.get('userid')
        tenderNo = request.POST.get('tenderNo')
        secret_key = "admin"
        encoder_decoder = HmacEncoderDecoder(secret_key)
        encoded_data = encoder_decoder.encode_data({'userid': userId, 'transaction': cotedAmount})
        print("Encoded data:", encoded_data)
        print(tenderNo)
        decoded_data = encoder_decoder.decode_data(encoded_data)
        print("Decoded data:", decoded_data)
        participant_info = getattr(request, 'participant_info', None)
        tenders = getattr(request, 'tenderList', None)
        previousHash = blockchain_count()
        out = tenderCotated.objects.filter(tenderid=tenderNo,userid=userId).exists()
        if out:
            return redirect('/dashboard')
        else:
            createBlockchain(tenderNo,previousHash,encoded_data['digest'],encoded_data)
            tenderCote_create(tenderNo,userId)
    return render(request, "e-participant/index.html", {'participant_info': participant_info,'tenders':tenders},)

def createBlockchain(tenderNo,previousHash,encoded,data ):
    blockchain_data = Blockchain.objects.create(
                tenderid=tenderNo,  
                previousHash=previousHash,
                currentHash= encoded,
                data = data
            )
    tt = blockchain_data.save()
    print("Blockchain data saved successfully!")
    return blockchain_data

def tenderCote_create(tenderNo,userId):
    tender_cotated = tenderCotated.objects.create(
                tenderid=tenderNo,  
                userid=userId,
            ) 
    tender_cotated.save()
    print("tender cotated data saved successfully!")
    return tender_cotated

def blockchain_count():
    previousHash = 0
    totalCount = Blockchain.objects.count()
    if(totalCount>0):
        last_row_data = Blockchain.objects.last()
        previousHash = last_row_data.currentHash
    return previousHash