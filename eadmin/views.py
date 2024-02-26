from django.shortcuts import render,redirect
from .models import particpantForm,LoginParticpantForm,particpants,tender,Blockchain,tenderCotated,TenderForm
from datetime import datetime
from django.http import HttpResponseRedirect

from django.contrib import messages
from .HmacEncoderDecoder import HmacEncoderDecoder
import json
import pickle
import random
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    data=[]
    tendersList = tender.objects.filter(status=False)
    for tt in tendersList:
        print(tt.title)
        winnerid = tt.winnerid
        blid = tt.blockid
        participantInfo = particpants.objects.filter(id=winnerid)
       
        blockInfo = Blockchain.objects.filter(id=blid)
        transaction = 0
        for bb in blockInfo:
            # Assuming bb.data is a dictionary
            obj = bb.data
            # Access the keys and values directly
            transaction = obj['data']['transaction']
        data.append({'title':tt.title,'tenderNo':tt.tenderNo,'img':tt.img,'Initalcotation':tt.initalCotation,'winnerName':participantInfo[0].username,'transaction':transaction}) 
    print(data)
    return render(request,"common/index.html",{"winnerList":data})

def login(request):
    if request.method == 'POST':
        form = LoginParticpantForm(data= request.POST)      
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if email=="authority@blockchain.com" and password=="authority":
                return redirect('viewTenderList')
            else:
                particpant = particpants.objects.get(email=email)
                if particpant.password==password:
                    request.session['user_id']  = particpant.id  
                    messages.success(request, 'Login successful!')
                    return redirect('dashboard') 
                else:
                    return redirect('login') 
    else:
        form = LoginParticpantForm()

    return render(request,"common/loginPage.html", {'form':form})

def register(request):
    message = ''
    if request.method == 'POST':
        form = particpantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')
        else:
            messages.error(request,"Invalid form submission")
    else:
        form = particpantForm()
    return render(request,"common/registerPage.html",{'form':form})

def dashboard(request):
    participant_info = getattr(request, 'participant_info', None)
    if not participant_info:
        return redirect('login')  # Redirect to login if participant_info is not available
    logger.warning(str(participant_info.id))  # Log participant ID
    tenders = getattr(request, 'tenderList', None)
    newtenders = []
    logger.warning(f"Tenders: {tenders}") 
    btn_status= False
    today_date = datetime.today().date()
    for tend in tenders:
        print(tend.started_at.date())
        if tend.started_at.date()==today_date or tend.started_at.date()<today_date:
            btn_status= True
        newtenders.append({'id':tend.id,'title':tend.title,'img':tend.img,'started_at':tend.started_at,'ended_at':tend.ended_at,'status':btn_status,"initalCotation":tend.initalCotation})
    print("Today's date is:", today_date)
    return render(request, "e-participant/index.html", {'participant_info': participant_info,'tenders':newtenders},)

    
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
    print(participant_info.id)
    currentUserid = 0
    isCotated = False
    for bbl in bl_block:
        if int(bbl['userid']) == participant_info.id:
            print("already cotated")
            isCotated = True
        else:
            print("not quoted")

    return render(request,'e-participant/tenderDetails.html',{'tenderDetails':tenders,'block_list': bl_block, 'participant_info': participant_info,"isCotated":isCotated})


def newCotation(request):
    message = "" 
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
            message = "Bid successfully"
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

def viewUsers(request):
    users = getattr(request, 'userList', None)
    return render(request,"e-admin/UserList.html",{"userList":users})

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

def NetworkAttackLogin(request):
    if request.method == 'POST':
        form = LoginParticpantForm(data= request.POST)  
        output = predictAttack() 
        print("line 215:",output)  
        if output == 0:
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
                        return redirect('login') 
        else:
            return render(request, "common/attack_detected.html") 
    else:
        form = LoginParticpantForm()
    return render(request,"common/AttackLogin.html", {'form':form})


def predictAttack():
    categories =  pickle.load(open('model/categoricalValues.sav', 'rb'))
    ddosCategoryValue =  pickle.load(open('model/ddos_Category_data.sav', 'rb'))
    trafficCategoryValue =  pickle.load(open('model/traffic_Category_data.sav', 'rb'))
    test_data = [
    [0.0,'icmp', 'netbios_dgm', 'RSTO',  304.0,  8343.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  2.0,  255.0,  1.0,  0.0,  0.5,  0.01,  0.0,  0.0,  0.0,  0.0],
    [0,'tcp','discard','S0',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,256,2,1.00,1.00,0.00,0.00,0.01,0.05,0.00,255,2,0.01,0.05,0.00,0.00,1.00,1.00,0.00,0.00],
    [33.0,  'tcp', 'telnet',  'SF',  2402.0,  3815.0,  0.0,  0.0,  0.0,  3.0,  0.0,  1.0,  2.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  1.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  3.0,  3.0,  1.0,  0.0,  0.33,  0.0,  0.0,  0.0,  0.0,  0.0],
    [49.0,  'tcp', 'telnet',  'SF',  2402.0,  3939.0,  0.0,  0.0,  0.0,  4.0,  0.0,  1.0,  2.0,  1.0,  0.0,  0.0,   0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  1.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  2.0,  1.0,  0.0,  1.0,  1.0,  0.0,  0.0,  0.0,  0.0]
    ]
    testInput = random.choice(test_data)
    print(testInput)
    testInput[1] = categories[0][testInput[1]]
    testInput[2] = categories[2][testInput[2]]
    testInput[3] = categories[1][testInput[3]]
    testList =[testInput]
    rf_traffic_loaded_model = pickle.load(open('model/catboost_traffic.sav', 'rb'))
    myResult = rf_traffic_loaded_model.predict(testList)
    result = 0
    if(myResult[0] == 0):
        rf_ddos_loaded_model = pickle.load(open('model/catboost_ddos.sav', 'rb'))
        ddosResult = rf_ddos_loaded_model.predict(testList)
        value = [i for i in ddosCategoryValue if ddosCategoryValue[i]==ddosResult[0]][0]
        print('Based on Url Parameters the attack is detected as ddos attack')
        print('-------------------------------------------------------------')
        print('-------------------------------------------------------------')
        print('--Blocking the IP Address------------------------------------')
        print('-------------------------------------------------------------')
        print('-------------------------------------------------------------')
        print('-------------------------------------------------------------')
        print('-------------------------------------------------------------')
        result = 1
        print("The traffic is identified as ddos category is "+value)
    elif(myResult[0] == 4):
        result = 0
        print('normal- Request Processing')
    else:
        result = 2
        print('block the request, malicious traffic')
    return result
    
def attack_page(request):
    return render(request,'common/attack_detected.html')

