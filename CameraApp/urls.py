from django.urls import path
from .import views

app_name = 'CameraApp'

urlpatterns = [
    path('', views.Index ,name ='index'),
    path('create', views.UserCreateView, name = 'create'),
    path('video_feed', views.video_feed, name = 'video_feed')
]
