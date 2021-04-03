from django.shortcuts import render,redirect
from django.http import StreamingHttpResponse, HttpResponse
import pandas as pd
from datetime import datetime
from CameraApp.camera import VideoCamera
from .models import Status, Patient
from .forms import PatientForm

from rest_framework.decorators import api_view
from .serializers import PatientSerializer, StatusSerializer
from rest_framework.response import Response

import pytz
tz = pytz.timezone('Asia/Kolkata')

# Create your views here.

################################################################################################################
####################################    for streaming camera ###################################################
################################################################################################################

def gen(camera):
    while True:
	    frame = camera.get_frame()
	    yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')

################################################################################################################
########################################     INDEX VIEW       ##################################################
################################################################################################################

def Index(request):    
    name = '' 
    person = ''
    stat = ''
    ##########################   Fetching recent person is known or unknown  #####################
    s_obj = Status.objects.latest('pk')
    status = s_obj.status

    #################################   FOR UNKNOWN USERS     ####################################
    if status.lower() == 'unknown':   
        print('An unknown detected') 

        obj_time = s_obj.created_at        
        time2 = obj_time.astimezone(tz)       
        time3 = time2.replace(tzinfo = None)
        now = datetime.now()   

        dif = (now-time3).seconds
        print(dif)

        if dif<=30:
            print('new Unknown Person Identified')
            stat = 'new'
        else:
            print('unknown person identified long time ago')
            stat = 'old'

    ################################    FRO KNOWN PERSONS     #####################################
    elif status.lower() == 'known':        
        data = pd.read_csv('E:/WEB_PROJECTS/Smile_FR_Project/FR_ML_CODE/Id.csv')   
        # print(data) 
        l = len(data)    
        last_person = data.loc[l-1]  
        name = last_person['name']   
        date = last_person['date']
        now = datetime.now()
        recent_date = datetime.strptime(date, '%d-%m-%Y %H:%M:%S')
        diff = (now-recent_date).seconds

        print(diff)

        if diff<=25:
            print('person detected recently')
            person = 'recent'
        else:
            print('person detected long time ago')
            person = 'ago'

        return render(request,'CameraApp/index.html', {'name':name, 'date':date, 'status':status, 'person': person})  
    else:
        return HttpResponse('Page Not Found') 
    return render(request,'CameraApp/index.html', {'status':status, 'stat':stat})

        
#################################################################################################################
###################################      USER CREATE VIEW     ###################################################
#################################################################################################################

def UserCreateView(request):
    if request.method == 'POST':
        form  = PatientForm(request.POST)
        if form.is_valid():
            
            pat = Patient.objects.create(first_name = request.POST['first_name'],
                                        last_name = request.POST['last_name'],
                                        age = request.POST['age'],
                                        blood_group = request.POST['blood_group'],
                                        gender = request.POST['gender'],
                                        status = request.POST['status'],
                                        contact = request.POST['contact'],
                                        email = request.POST['email'],
                                        city = request.POST['city']
                                        )
            pat.save()
            st = Status.objects.latest('pk')
            if st.status == 'unknown':                
                st.delete()
                print('recent unkown feeded')
            else:
                print('recent is known') 

            return redirect('CameraApp:index')
    else:
        form = PatientForm()
    return render(request, 'CameraApp/create.html', {'form':form})

#############################################################################################################
##########################################  API VIEWS   #####################################################
#############################################################################################################

@api_view(['GET'])
def apiView(request):
    api_urls = {
        'recent-patient' : '/api/patients',
        'recent-status'  : '/api/status-recent',
        'all-patients'   : '/api/all-patients',
        'all-status'     : '/api/status',
        'create-patient' : '/api/create-patient',
        'create-status'  : '/api/create-status',
    }
    return Response(api_urls)

@api_view(['GET'])
def recentPatient(request):
    pat = Patient.objects.latest('pk')
    serializer = PatientSerializer(pat, many = False)
    return Response(serializer.data)

@api_view(['GET'])
def recentStatus(request):
    stat = Status.objects.latest('pk')
    serializer = StatusSerializer(stat, many = False)
    return Response(serializer.data)

@api_view(['GET'])
def StatusRest(request):
    stat = Status.objects.all().order_by('-id')
    serializer = StatusSerializer(stat, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def allPatients(request):
    pats = Patient.objects.all().order_by('-id')
    serializer = PatientSerializer(pats, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def createStatus(request):
    serializer = StatusSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def createPatient(request):
    serializer = PatientSerializer(request.data)
    if serializer.is_valid():
        serializer.save()
    return  Response(serializer.data)

###########################################################################################
#############################    ACCOUNTS VIEWS   #########################################
###########################################################################################

