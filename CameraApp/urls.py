from django.urls import path
from .import views

app_name = 'CameraApp'

urlpatterns = [
    path('', views.Index ,name ='index'),
    path('video_feed', views.video_feed, name = 'video_feed')
]
