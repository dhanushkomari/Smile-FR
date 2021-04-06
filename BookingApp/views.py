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
    op = 'q'
    time = ''
    name = 'Dhanus'
    b = Booking.objects.all()
    for i in range(len(b)):
        obj = b[i].patient.first_name
        if obj == name:
            print(b, 'is Existed')
            op = 'yes'
            time = b[i].Booking_time
            print(time)
            break

    if op ==  'q':
        print('Not exist with name')
    
            
    return render(request, 'BookingApp/test.html')