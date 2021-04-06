from django.db import models
from CameraApp.models import Patient

# Create your models here.

########################################################################################
##############################     DEPARTMENT MODEL     ################################
########################################################################################
class Department(models.Model):
    name = models.CharField(max_length = 20, unique = True, null = False, blank = False)
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ('-id',)

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
        pass

########################################################################################
##############################       DOCTOR MODEL       ################################
########################################################################################
class Doctor(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    designation = models.CharField(max_length = 25)
    contact = models.CharField(max_length = 11)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    Photo = models.ImageField(upload_to='doctors')

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        ordering = ('-id',)

    def __str__(self):
        return '{}'.format(self.first_name +' '+self.last_name)

    def get_url(self):
        pass

########################################################################################
#############################       BOOKINGS MODEL      ################################
########################################################################################
time =(
        ('10:00 to 10:30', '10:00 to 10:30'),
        ('10:30 to 11:00', '10:30 to 11:00'),
        ('11:00 to 11:30', '11:00 to 11:30'),
        ('11:30 to 12:00', '11:30 to 12:00'),
        ('12:00 to 12:30', '12:00 to 12:30'),
        ('12:30 to 01:00', '12:30 to 01:00'),
        ('18:00 to 18:30', '18:00 to 18:30'),
        ('18:30 to 19:00', '18:30 to 19:00'),
        ('19:00 to 19:30', '19:00 to 19:30'),
        
)
class Booking(models.Model):    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    description = models.TextField()
    Booking_time = models.CharField(default = '10:00 to 10:30', choices = time, max_length = 15)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ('-id',)

    def __str__(self):
        return '{}'.format(self.id)

    def get_url(self):
        pass
    
    


