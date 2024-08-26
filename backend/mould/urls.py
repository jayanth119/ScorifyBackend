from django.urls import path
from .views import LandlordMouldView,VentilationItemView,TenantMouldView
urlpatterns=[
    path('landlord/<uuid:uuid_id>/mould/',LandlordMouldView.as_view(),name='landlord-mould'),
    path('tenant/ventilation-image/upload/',VentilationItemView.as_view(),name="ventilation-image-upload"),
    path('tenant/ventilation-image/',VentilationItemView.as_view(),name="ventilation-image"),
    path('tenant/mould/',TenantMouldView.as_view(),name='tenant-moould')
]