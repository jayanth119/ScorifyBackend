from django.db import models
import uuid 
from core.models import Property 
from django.contrib.auth import get_user_model

customuser = get_user_model()
class Maintenance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(customuser,on_delete=models.CASCADE,related_name='maintenance')
    score = models.FloatField()
    details = models.TextField()
    completion_date = models.DateField()
    status = models.CharField(max_length=50)
    report_photos = models.FileField(upload_to='maintenance/',null=True,blank=True)
    report = models.TextField()
    performed_by = models.CharField(max_length=255)
    history = models.TextField()
    due_date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    upcoming_photo = models.FileField(upload_to='maintenance/upcoming/',null=True,blank=True)


    def __str__(self):

        return f'Maintenance - {self.id} - {self.status}'
class MaintenanceImage(models.Model):
    maintenance = models.ForeignKey(Maintenance,related_name='images',on_delete=models.CASCADE)
    image =  models.ImageField(upload_to='maintenance_images/')
   
class Repair(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(customuser,on_delete=models.CASCADE,related_name='repair')
    property = models.ForeignKey(Property, on_delete=models.CASCADE,related_name='repair')
    repair_score = models.FloatField()
    repair_history = models.TextField()
    completion_date = models.DateField()
    status = models.CharField(max_length=50)
    description = models.TextField()
    completion_report = models.TextField()
    cost = models.FloatField()
    reported_by = models.CharField(max_length=255)

    def __str__(self):
        return f'Repair  - {self.status}'