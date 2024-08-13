from rest_framework import serializers
from .models import EPCReport

class EPCReportSerializer(serializers.ModelSerializer):
    view_document = serializers.FileField(source='document', read_only=True)
    download_document = serializers.FileField(source='document', read_only=True)

    class Meta:
        model = EPCReport
        fields = ['report_date', 'report', 'current_score', 'potential_score', 'view_document', 'download_document']
