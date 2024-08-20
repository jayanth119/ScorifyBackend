from django.db import models
import uuid 
from core.models import Property  
from django.contrib.auth import get_user_model
# Create your models here.
customUser = get_user_model()
class MouldHumidity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(customUser,on_delete=models.CASCADE)
    avg_humidity_30_days = models.FloatField()
    ventilation_score = models.FloatField()
    condition = models.CharField(max_length=255)
    temperature = models.FloatField()
    humidity = models.FloatField()
    mould_presence_90_days = models.JSONField()  
    previous_ventilation_date = models.DateField()
    next_ventilation_date = models.DateField()

    def __str__(self):
        return f'Mould Humidity - {self.property}'

class VentilationItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Ventilation - {self.id}"

class VentilationImages(models.Model):
    item = models.ForeignKey(VentilationItem,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='media/ventilation/')