from django.urls import path
from .mixins import AgentServiceList,TenantServiceList,LandlordServiceList
from .views import LandlordScheduleList,AgentScheduleList,TenantScheduleList,LandlordUpcomingList,AgentOpenRepairView,LandlordOpenRepairView,TenantOpenRepairView,TenantRepairHistoryView
urlpatterns =[
    path('landlord/regular-maintenance/service-history/',LandlordServiceList.as_view(),name="landlord-service-history"),
    path('agent/regular-maintenance/service-history/',AgentServiceList.as_view(),name="agent-service-history"),
    path('tenant/regular-maintenance/service-history/',TenantServiceList.as_view(),name="tenant-service-history"),
    path('landlord/regular-maintenance/schedule/',LandlordScheduleList.as_view(),name="landlord-schedule"),
    path('agent/regular-maintenance/schedule/',AgentScheduleList.as_view(),name="agent-schedule"),
    path('tenant/regular-maintenance/schedule/',TenantScheduleList.as_view(),name="tenant-schedule"),
    path('landlord/regular-maintenance/upcoming-service/',LandlordUpcomingList.as_view(),name="tenant-upcoming-service"),
    path('agent/open-repairs/',AgentOpenRepairView.as_view(),name='agent-open-repair'),
    path('landlord/repair-history/',LandlordOpenRepairView.as_view(),name='landlord-repair-history'),
    path('tenant/repair-history/',TenantRepairHistoryView.as_view(),name='tenant-repair-history'),
    path('tenant/open-repairs/',TenantOpenRepairView.as_view(),name='tenant-open-repairs'),

]
