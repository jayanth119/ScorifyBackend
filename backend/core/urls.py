from django.urls import path
from core.views import LandlordDetailView, TenantDetailView, AgentDetailView, LandlordListView, TenantListView, AgentListView, PropertyListView , PropertyDetailView , LandlordDashboardView , TenantDashboardView,HousePhotoView
from .views import LandlordReportUploadView
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    # Landlord URLs
    path('landlords/', LandlordListView.as_view(), name='landlord-list'),
    path('landlords/<uuid:id>/', LandlordDetailView.as_view(), name='landlord-detail'),

    # Tenant URLs
    path('tenants/', TenantListView.as_view(), name='tenant-list'),
    path('tenants/<uuid:id>/', TenantDetailView.as_view(), name='tenant-detail'),

    # Agent URLs
    path('agents/', AgentListView.as_view(), name='agent-list'),
    path('agents/<uuid:id>/', AgentDetailView.as_view(), name='agent-detail'),
     path('properties/', PropertyListView.as_view(), name='property-list'),
    path('c/<uuid:id>/', PropertyDetailView.as_view(), name='property-detail'),
    path('landlords/<uuid:landlord_uuid>/upload-report/', csrf_exempt(LandlordReportUploadView.as_view()), name='upload-report'),
    path('tenant-dashboard/<uuid:tenant_id>/', TenantDashboardView.as_view(), name='tenant_dashboard'),
    path('landlord-dashboard/<uuid:landlord_id>/', LandlordDashboardView.as_view(), name='landlord_dashboard'),
    path('tenant/house-photo/',HousePhotoView.as_view(),name="house-photo"),
    path('tenant/<uuid:property_id>/house-photo/',HousePhotoView.as_view(),name="house-photo-upload")

]


