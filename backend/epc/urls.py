from django.urls import path
from .views import LatestEPCReportView, EPCReportListView,EPCScoreLast12MonthsView,EPCGradeCountView


urlpatterns = [
    path('landlords/epc/latest/<uuid:property_id>', LatestEPCReportView.as_view(), name='latest-epc-report'),
    path('landlords/epc/reports/<uuid:property_id>', EPCReportListView.as_view(), name='epc-report-list'),
    path('landlords/epc/scores/<uuid:property_id>', EPCScoreLast12MonthsView.as_view(), name='epc-scores-last-12-months'),
    path('agents/epc/grades/count/<uuid:agent_id>/', EPCGradeCountView.as_view(), name='epc-grade-count'),

]

