from django.db import models
import uuid
from core.models import Property

class EPCReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    score = models.FloatField()  # Assume this is now a float for EPC score as a number
    report_date = models.DateField()
    report = models.TextField()
    current_score = models.FloatField()  # Assuming numerical scores for current and potential scores
    potential_score = models.FloatField()
    document = models.FileField(upload_to='epc_reports/', null=True, blank=True)

    def __str__(self):
        return f'EPC Report - {self.property} - {self.report_date}'
