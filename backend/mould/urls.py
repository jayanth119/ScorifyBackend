from django.urls import path
from .views import LandlordMouldView,VentilationItemView,VentilationDetailView
urlpatterns=[
    path('landlord/<uuid:uuid_id>/mould/',LandlordMouldView.as_view(),name='landlord-mould'),
    path('tenant/ventilation-image/upload/',VentilationItemView.as_view(),name="ventilation-image-upload"),
    path('tenant/ventilation-image/',VentilationDetailView.as_view(),name="ventilation-image"),
]