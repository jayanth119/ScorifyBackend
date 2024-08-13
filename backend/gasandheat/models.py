from django.db import models
from core.models import Property 
# Create your models here.
import uuid



class GasSafety(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    repair_score = models.FloatField()
    report_date = models.DateField()
    title = models.CharField(max_length=255)
    current_eer = models.FloatField()
    potential_eer = models.FloatField()
    due_date = models.DateField()
    expiry_months = models.IntegerField()

    def __str__(self):
        return f'Gas Safety - {self.property}'

class HeatingSafety(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    repair_score = models.FloatField()
    boiler_condition = models.CharField(max_length=255)
    controller = models.CharField(max_length=255)
    radiators_condition = models.CharField(max_length=255)
    flue_ventilation_condition = models.CharField(max_length=255)

    def __str__(self):
        return f'Heating Safety - {self.property}'