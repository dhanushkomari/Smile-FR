from django.shortcuts import render,redirect
from django.http import StreamingHttpResponse, HttpResponse
import pandas as pd
from CameraApp.camera import VideoCamera
from .models import Status, Patient
from .forms import PatientForm

from rest_framework.decorators import api_view
from .serializers import PatientSerializer, StatusSerializer
from rest_framework.response import Response

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
    ##########################   Fetching recent person is known or unknown  #####################
    s_obj = Status.objects.latest('pk')
    status = s_obj.status

    if status.lower() == 'unknown':   
        print('An unknown detected')     
        # return redirect('CameraApp:create')

    elif status.lower() == 'known':        
        #####################     fetching recent person  #####################
        data = pd.read_csv('E:/WEB_PROJECTS/Smile_FR_Project/FR_ML_CODE/Id.csv')   
        # print(data) 
        l = len(data)    
        last_person = data.loc[l-1]  
        name = last_person['name']   
        date = last_person['date']
        
        return render(request,'CameraApp/index.html', {'name':name, 'date':date, 'status':status})  
    else:
        return HttpResponse('Page Not Found') 
    return render(request,'CameraApp/index.html', {'status':status})


        
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
def recentPatient(request):
    pat = Patient.objects.latest('pk')
    serializer = PatientSerializer(pat, many = False)
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