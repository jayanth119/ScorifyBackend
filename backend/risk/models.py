from django.db import models
import uuid 
from core.models import Property 
# Create your models here.



class SafetyAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    score = models.FloatField()
    electricity_condition = models.CharField(max_length=255)
    gas_condition = models.CharField(max_length=255)
    structural_integrity = models.CharField(max_length=255)
    mould_damp_condition = models.CharField(max_length=255)
    asbestos_condition = models.CharField(max_length=255)
    security_risk = models.CharField(max_length=255)
    report = models.TextField()

    def __str__(self):
        return f'Safety Assessment - {self.property}'

class RiskAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    document = models.TextField()
    date = models.DateField()
    document_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    expiry_date = models.DateField()

    def __str__(self):
        return f'Risk Assessment - {self.property}'

