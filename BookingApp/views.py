from django.shortcuts import render
from .forms import BookingForm
from .models import Booking
from CameraApp.models import Patient


# Create your views here.

def BookingView(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            p = request.POST['patient']
            print(p)

            book = Booking.objects.create(patient= request.POST['patient'],
                                          doctor = request.POST['doctor'],
                                          description = request.POST['description'],
                                          Booking_time = request.POST['Booking_time']
                                            )
            book.save()
    else:
        form = BookingForm()
    return render(request, 'BookingApp/booking.html', {'form':form})


def test(request):
    name = 'Dhanu'
    p = Booking.objects.filter(patient__first_name__contains = name).latest('pk')
    print(p)
    print(p.patient.first_name)
    print(p.patient.last_name)
    print(p.created_at)
    print(p.Booking_time)

            
    return render(request, 'BookingApp/test.html')