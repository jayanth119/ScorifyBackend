from django.urls import path
from .views import LandlordScheduleList,TenantScheduleList,AgentOpenRepairView,LandlordRepairHistoryView,LandlordMaintenanceServiceHistory,AgentMaintenanceView,TenantRepairHistoryView ,  TenantInspectionView

urlpatterns =[
    path('landlord/<uuid:user_id>/regular-maintenance/service-history/',LandlordMaintenanceServiceHistory.as_view(),name="landlord-service-history"),
    # path('agent/regular-maintenance/service-history/',AgentServiceList.as_view(),name="agent-service-history"),
    # path('tenant/regular-maintenance/service-history/',TenantServiceList.as_view(),name="tenant-service-history"),
    path('tenant/<uuid:user_id>/repair-history/',TenantRepairHistoryView.as_view(),name="tenant-repair-history"),
    path('landlord/<uuid:user_id>/regular-maintenance/schedule/',LandlordScheduleList.as_view(),name="landlord-schedule"),
    path('agent/<uuid:user_id>/regular-maintenance/',AgentMaintenanceView.as_view(),name="agent-regular-maintenance"),
    path('tenant/regular-maintenance/schedule/<uuid:tenant_id>/',TenantScheduleList.as_view(),name="tenant-schedule"),
    path('tenant/regular-maintenance/schedule/upload/<uuid:tenant_id>/',TenantScheduleList.as_view(),name="tenant-schedule"),
  
    path('agent/<uuid:user_id>/open-repairs/',AgentOpenRepairView.as_view(),name='agent-open-repair'),
    path('landlord/<uuid:user_id>/repairs/', LandlordRepairHistoryView.as_view(), name='landlord-repair-history'),
    path('tenant/<uuid:tenant_id>/inspect/', TenantInspectionView.as_view(), name='tenant-inspection'),


]

