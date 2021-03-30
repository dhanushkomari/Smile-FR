from django.db import models

# Create your models here.
class Status(models.Model):
    status = models.CharField(max_length = 10, blank = True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
        ordering = ('created_at',)

    def __str__(self):
        return '{}'.format(self.status)

