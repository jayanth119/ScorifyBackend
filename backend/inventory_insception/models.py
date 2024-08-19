from django.db import models
import uuid 
from core.models import Property
# Register your models here.

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, related_name='inventory', on_delete=models.CASCADE)
    document = models.TextField()
    score = models.FloatField()
    date = models.DateField()
    type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    expiry_date = models.DateField()
    past_inventory = models.BooleanField()

    def __str__(self):
        return f'{self.title} - {self.property} - {self.date}'

class Room(models.Model):
    inventory = models.ForeignKey(Inventory, related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    completion_percentage = models.FloatField(default=0.0)
                                        
    def __str__(self):
        return f'{self.name} - {self.inspection}'

class Condition(models.Model):
    room = models.ForeignKey(Room, related_name='conditions', on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    condition = models.CharField(max_length=10, choices=[('good', 'Good'), ('fair', 'Fair'), ('repair', 'Repair')])
    cleanliness= models.CharField(max_length=10,choices=[('good','Good'),('fair','Fair'),('poor','Poor')],default='good')
    photo = models.ImageField(upload_to='room_conditions/', blank=True, null=True)
    # document = models.FileField(upload_to='condition_documents/', blank=True, null=True)

    def __str__(self):
        return f'{self.item} - {self.room} - {self.condition}'

class Defect(models.Model):
    room=models.ForeignKey(Room,related_name='defects',on_delete=models.CASCADE)
    description=models.TextField()
    def __str__(self):
        return f'{self.description[:40]}...-{self.room}'



