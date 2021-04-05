from django.shortcuts import render

# Create your views here.

def  BookingView(request):
    return render(request, 'BookingApp/booking.html')
