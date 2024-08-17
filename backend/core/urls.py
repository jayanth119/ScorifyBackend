from django.urls import path
from core.views import LandlordDetailView, TenantDetailView, AgentDetailView, LandlordListView, TenantListView, AgentListView, PropertyListView , PropertyDetailView

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
]
