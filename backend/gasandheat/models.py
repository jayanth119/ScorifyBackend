from django.db import models
from core.models import Property 
import uuid
import os
from django.conf import settings

def gas_safety_upload_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/gassafety/<property_id>/<filename>
    return os.path.join('gassafety', str(instance.property.id), filename)

class GasSafety(models.Model):
    EER_CHOICES = [(chr(65 + i), chr(65 + i)) for i in range(7)]  # A to G

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    repair_score = models.FloatField()
    report_date = models.DateField()
    due_date = models.DateField()
    expiry_months = models.IntegerField()
    current_eer = models.CharField(max_length=1, choices=EER_CHOICES)  # A to G
    potential_eer = models.CharField(max_length=1, choices=EER_CHOICES)  # A to G
    document = models.FileField(upload_to=gas_safety_upload_path, null=True, blank=True)

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