from django.shortcuts import render,redirect
from django.http import StreamingHttpResponse, HttpResponse
import pandas as pd
from CameraApp.camera import VideoCamera
from .models import Status

# Create your views here.

####################################    for streaming camera ###################################################
def gen(camera):
    while True:
	    frame = camera.get_frame()
	    yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')

################################################################################################################

def Index(request):    
    name = ''   

    ###################   Fetching recent person is known or unknown  #####################

    s_obj = Status.objects.latest('pk')
    status = s_obj.status

    if status.lower() == 'unknown':   
        print('An unknown detected')     
        return render(request, 'CameraApp/create.html')

    elif status.lower() == 'known':
        
        ###### fetching recent person ######
        data = pd.read_csv('E:/WEB_PROJECTS/Smile_FR_Project/FR_ML_CODE/Id.csv')   
        print(data) 
        l = len(data)    
        last_person = data.loc[l-1]    
        name = last_person['name']
        date = last_person['date']
    else:
        return HttpResponse('Page Not Found')    
    return render(request,'CameraApp/index.html', {'name':name, 'date':date, 'status':status})
    #####################################################################################



def UserCreateView(request):
    return render(request, 'CameraApp/create.html')