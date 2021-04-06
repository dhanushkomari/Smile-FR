from django.urls import path
from . import views

app_name = "BookingApp"

urlpatterns = [
    # path('', views.BookingView, name = 'booking'),
    # path('', views.test, name = 'test'), 
    path('<str:pk>', views.ShowBookingView, name = 'single-booking')
]
