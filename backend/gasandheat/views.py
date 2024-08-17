from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import GasSafety 
from core.models import Property
class CurrentGasSafetyView(View):
    def get(self, request, property_id):
        # Get the most recent Gas Safety report for the given property
        latest_report = GasSafety.objects.filter(property_id=property_id).order_by('-report_date').first()

        if latest_report:
            # Calculate expiry months dynamically
            current_date = timezone.now().date()
            expiry_months = relativedelta(latest_report.due_date, current_date).months + \
                            12 * (latest_report.due_date.year - current_date.year)

            data = {
                "report_date": latest_report.report_date,
                "repair_score": latest_report.repair_score,
                "expiry_months": expiry_months,
                "view_document": latest_report.document.url if latest_report.document else None,
                
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"detail": "No Gas Safety report found for this property."}, status=404)


class PreviousGasSafetyReportsByPropertyView(View):
    def get(self, request, property_id):
        # Get all Gas Safety reports for the given property, excluding the latest one
        reports = GasSafety.objects.filter(property_id=property_id).order_by('-report_date')[1:]  # Skip the first (latest) report

        if reports.exists():
            data = [
                {
                    "property_id": report.property.id,
                    "property_address": report.property.address,
                    "report_date": report.report_date,
                    "repair_score": report.repair_score,
                    "current_eer": report.current_eer,
                    "potential_eer": report.potential_eer,
                    "expiry_months": relativedelta(report.due_date, timezone.now().date()).months + \
                                    12 * (report.due_date.year - timezone.now().date().year),
                    "view_document": report.document.url if report.document else None,
                }
                for report in reports
            ]
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"detail": "No previous Gas Safety reports found for this property."}, status=404)

