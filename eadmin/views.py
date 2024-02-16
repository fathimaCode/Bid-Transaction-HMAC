from django.shortcuts import render,redirect
from .models import particpantForm,LoginParticpantForm,particpants,tender,Blockchain,tenderCotated,TenderForm
import datetime
from django.contrib import messages
from .HmacEncoderDecoder import HmacEncoderDecoder
import json

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
            if email=="authority@blockchain.com" and password=="authority":
                return redirect('authority_newTender')
            else:
                particpant = particpants.objects.get(email=email)
                if particpant.password==password:
                    request.session['user_id']  = particpant.id  
                    messages.success(request, 'Login successful!')
                    return redirect('dashboard') 
    else:
        form = LoginParticpantForm()
    if request.method == 'POST' and not form.is_valid():
        # If the form submission took longer than the timeout, redirect to a page indicating attack
        return render(request, "common/attack_detected.html")
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
    bl_block = isTenderCotatedByUser(tender_id)
   # block_list = getattr(request, 'block_list', None)
    participant_info = getattr(request, 'participant_info', None)
    return render(request,'e-participant/tenderDetails.html',{'tenderDetails':tenders,'block_list': bl_block, 'participant_info': participant_info})


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
        message = "Already Cotated"
        if out:
            return redirect('/dashboard')
        else:
            createBlockchain(tenderNo,previousHash,encoded_data['digest'],encoded_data)
            tenderCote_create(tenderNo,userId)
            message = "created successfully"
    return render(request, "e-participant/index.html", {'participant_info': participant_info,'tenders':tenders,'message':message})

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

def displayBlockchain_blocks(tender_id):
    blocks=Blockchain.objects.filter(tenderid=tender_id)
    return blocks

def isTenderCotatedByUser(tender_id):
    blocks=Blockchain.objects.filter(tenderid=tender_id)
    cotation = []
    isactive =False
    for bb in blocks:
        # Assuming bb.data is a dictionary
        obj = bb.data
        # Access the keys and values directly
        currentUserid = obj['data']['userid']
        print("line 400:",bb.id)
        cotation.append({'bbid':bb.id,'userid':currentUserid,'tenderid':bb.tenderid,'transaction':obj['data']['transaction'],'previousHash':bb.previousHash,'currentHash':bb.currentHash,'updated_at':bb.updated_at})
    print(cotation)
    return cotation



#create an new tender
def authority_newTender(request):
    if request.method == 'POST':
        form = TenderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('authority_newTender')
    else:
        form = TenderForm()
    return render(request,"e-admin/index.html",{'form':form})

def viewTenderList(request):
    tenders = getattr(request, 'tenderList', None)
    return render(request,"e-admin/viewTenderList.html",{"tenderlist":tenders})

def deleteTender(request,tender_id):
    tenders=tender.objects.get(pk=tender_id)
    logger.warning(f"tender:{tenders}")
    tenders.delete()
    return redirect('viewTenderList')

def adminGetBidInfo(request,tender_id):
    tenders=tender.objects.get(pk=tender_id)
    logger.warning(f"tender:{tenders}")
    request.tender_id = tender_id
    bl_block = isTenderCotatedByUser(tender_id)
   # block_list = getattr(request, 'block_list', None)
    return render(request,'e-admin/BidInfo.html',{'tenderDetails':tenders,'block_list': bl_block})

def closeTender(request,tender_id):
    tenders=tender.objects.get(pk=tender_id)
    logger.warning(f"tender:{tenders}")
    tenders.status = False
    tenders.save()
    return redirect('viewTenderList')

def getBlockId(bbid):
    blocks=Blockchain.objects.filter(id=bbid)
    cotation = []
    isactive =False
    for bb in blocks:
        # Assuming bb.data is a dictionary
        obj = bb.data
        # Access the keys and values directly
        currentUserid = obj['data']['userid']
        print("line 400:",bb.id)
        cotation.append({'bbid':bb.id,'userid':currentUserid,'tenderid':bb.tenderid})
    print(cotation)
    return cotation

def announceWinner(request,blockid):
    tt = getBlockId(blockid)
    print(tt[0]['tenderid'])
    tenders=tender.objects.get(pk=tt[0]['tenderid'])
    logger.warning(f"tender:{tenders}")
    tenders.winnerid = tt[0]['userid']
    tenders.blockid = tt[0]['bbid']
    tenders.status= False
    tenders.save()
    return redirect('viewTenderList')

def networkAttack(request):
    return render(request,"common/attack_detected.html")