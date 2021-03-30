from django.shortcuts import render
from django.http import StreamingHttpResponse
import pandas as pd
from CameraApp.camera import VideoCamera

# Create your views here.

##############################    for streaming camera #############################################
def gen(camera):
    while True:
	    frame = camera.get_frame()
	    yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')
################################################################################################################



def Index(request):
    #######################################################

    ''''' fetching recent person '''''
    data = pd.read_csv('E:/WEB_PROJECTS/Smile_FR_Project/FR_ML_CODE/Id.csv')    
    l = len(data)    
    last_person = data.loc[l-1]    
    name = last_person['name']
    date = last_person['date']

    ''''' Fetching recent person is known or unknown  '''''





    #######################################################
    return render(request,'CameraApp/index.html', {'name':name, 'date':date})