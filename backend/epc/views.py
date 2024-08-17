from rest_framework import generics
from django.http import JsonResponse
from django.views import View
from .models import EPCReport
from .EpcSerializer import EPCReportSerializer
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
from django.db.models.functions import TruncMonth
from .models import EPCReport

from django.db.models import Count
from .models import EPCReport
from core.models import Agent 
# View to display the latest EPC report for a property
class LatestEPCReportView(generics.RetrieveAPIView):
    serializer_class = EPCReportSerializer

    def get_queryset(self):
        property_id = self.kwargs['property_id']
        return EPCReport.objects.filter(property_id=property_id).order_by('-report_date')

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.first()  # Return the latest report

    def get(self, request, *args, **kwargs):
        latest_report = self.get_object()
        if latest_report:
            data = {
                "report_date": latest_report.report_date,
                "report_description": latest_report.report,
                "current_epc": latest_report.current_score,
                "potential_epc": latest_report.potential_score,
                "epc_score": latest_report.score,  # Now returns a numeric value
                "view_document": latest_report.document.url if latest_report.document else None,
                "download_document": latest_report.document.url if latest_report.document else None,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"detail": "No EPC report found for this property."}, status=404)

# View to display all EPC reports for a property in JSON format
class EPCReportListView(View):
    def get(self, request, property_id):
        reports = EPCReport.objects.filter(property_id=property_id).order_by('-report_date')
        data = [
            {
                "report_date": report.report_date,
                "report_description": report.report,
                "current_epc": report.current_score,
                "potential_epc": report.potential_score,
                "epc_score": report.score,  # Now returns a numeric value
                "view_document": report.document.url if report.document else None,
                "download_document": report.document.url if report.document else None
            }
            for report in reports
        ]
        return JsonResponse(data, safe=False)




class EPCScoreLast12MonthsView(View):
    def get(self, request, property_id):
        # Calculate the date 12 months ago from today
        twelve_months_ago = timezone.now().date() - timedelta(days=365)

        # Aggregate the EPC scores by month
        reports = EPCReport.objects.filter(
            property_id=property_id,
            report_date__gte=twelve_months_ago
        ).annotate(month=TruncMonth('report_date')) \
         .values('month') \
         .annotate(average_epc_score=Avg('score')) \
         .order_by('month')

        # Prepare the response data
        data = [
            {
                "month": report['month'].strftime("%B"),
                "average_epc_score": report['average_epc_score']
            }
            for report in reports
        ]

        return JsonResponse(data, safe=False)




class EPCGradeCountView(View):
    def get(self, request, agent_id):
        # Get all properties related to the agent through the landlords they manage
        properties = EPCReport.objects.filter(
            property__landlords__agents__id=agent_id
        )

        # Aggregate the EPC grades (A to G) counts
        grade_counts = properties.values('score').annotate(count=Count('score')).order_by('score')

        # Prepare the response data
        grade_count_data = {grade['score']: grade['count'] for grade in grade_counts}

        # Ensure all grades A to G are included even if count is zero
        all_grades = {chr(65 + i): 0 for i in range(7)}  # A to G
        all_grades.update(grade_count_data)

        return JsonResponse(all_grades, safe=False)

