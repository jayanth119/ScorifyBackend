from django.db import models
import uuid 
from core.models import Property  
# Create your models here.

class MouldHumidity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    avg_humidity_30_days = models.FloatField()
    ventilation_score = models.FloatField()
    condition = models.CharField(max_length=255)
    temperature = models.FloatField()
    humidity = models.FloatField()
    mould_presence_90_days = models.JSONField()  # Stores an array of 90 values
    previous_ventilation_date = models.DateField()
    next_ventilation_date = models.DateField()

    def __str__(self):
        return f'Mould Humidity - {self.property}'
