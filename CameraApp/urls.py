from django.urls import path
from .import views

app_name = 'CameraApp'

urlpatterns = [
    path('', views.Index ,name ='index'),
    path('create', views.UserCreateView, name = 'create'),
    path('video_feed', views.video_feed, name = 'video_feed'),

    ##############   API URLS   ##############
    path('api/patients', views.recentPatient, name = 'recent_patient'),
    path('api/status', views.StatusRest, name = 'status'),
    path('api/all-patients', views.allPatients, name = 'all_patients')
]
