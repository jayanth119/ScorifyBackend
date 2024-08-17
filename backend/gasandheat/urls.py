from django.urls import path
from .views import CurrentGasSafetyView, PreviousGasSafetyReportsByPropertyView

urlpatterns = [
    path('landlords/gascur/<uuid:property_id>/', CurrentGasSafetyView.as_view(), name='current-gas-safety'),
    path('landlords/gasprev/<uuid:property_id>/', PreviousGasSafetyReportsByPropertyView.as_view(), name='previous-gas-safety-reports'),
]
