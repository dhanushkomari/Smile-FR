from django.contrib import admin
from .models import Status

# Register your models here.

class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'created_at']
    list_per_page = 20

admin.site.register(Status, StatusAdmin)

