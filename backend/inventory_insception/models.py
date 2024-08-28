from django.db import models
import uuid 
from core.models import Property,Landlord,Agent

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
        return f'{self.name} - {self.inventory}'

class Condition(models.Model):
    room = models.ForeignKey(Room, related_name='conditions', on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    iscomplete = models.BooleanField( default= False )
    description = models.CharField(max_length=256 , default="sample text")
    def __str__(self):
        return f'{self.item} - {self.room}'
class Inspection(models.Model):
    room = models.ForeignKey(Room, related_name='inspections', on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, related_name='inspections', on_delete=models.CASCADE, null=True, blank=True)
    property = models.ForeignKey(Property,related_name='inspections',on_delete=models.CASCADE)
    document = models.TextField()
    result = models.CharField(max_length=50)
    score = models.FloatField()
    created_by = models.CharField(max_length=255)
    due_date = models.DateField()
    date = models.DateField()
    is_completed = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Inspection for {self.room.name} - Due: {self.due_date} - Completed: {self.is_completed}'


class AgentLandlord(models.Model):
    agent=models.ForeignKey(Agent,on_delete=models.CASCADE,related_name='agentlandlord')
    landlord=models.ForeignKey(Landlord,on_delete=models.CASCADE,related_name='agentlandlord')

    class Meta:
        unique_together=('agent','landlord')
    
    def __str__(self):
        return f'{self.agent}-{self.landlord}'
    



        