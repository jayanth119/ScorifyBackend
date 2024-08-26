from django.urls import path
from . views import RoomList,RoomDetails,InventoryList,InventoryDetails,InventoryRooms,InventoryRoomDetails,AgentLandlordInventoryListView,AgentSpecificLandlordInventoryDetailView,TenantInventoryView,TenantRoomListView, TenantRoomDetailView, AgentInventoryView
from django.urls import path

urlpatterns = [
    path('rooms/',RoomList.as_view(),name='room-list'),   #Thiis 
    path('rooms/<uuid:room_id>/',RoomDetails.as_view(),name='room-detail'),   #This is the just for testing for getting rooms
   path('landlords/inventory/', InventoryList.as_view(), name='inventory-list'),  
    path('landlords/inventory/<uuid:inventory_id>/', InventoryDetails.as_view(), name='inventory-detail'),
     path('landlords/inventory/<uuid:inventory_id>/rooms/',InventoryRooms.as_view(),name='inventory-rooms'),
    path('landlords/inventory/<uuid:inventory_id>/rooms/<int:room_id>/',InventoryRoomDetails.as_view(),name='inventory-room-details'),   
    path('agent/<uuid:agent_id>/landlords/inventory/',AgentLandlordInventoryListView.as_view(), name='agent_landlords_inventory'),
    path('agent/<uuid:agent_id>/landlords/inventory/landlord/<uuid:landlord_id>/', AgentSpecificLandlordInventoryDetailView.as_view(), name='agent_specific_landlord_inventory'),
    # path('tenant/<uuid:tenant_id>/inventory/',TenantInventoryView.as_view(),name='tenant-inventory'),
    path('tenant/inventory/', TenantInventoryView.as_view(), name='tenant-inventory'),

    #  path('tenant/<uuid:tenant_id>/rooms/', TenantRoomListView.as_view(), name='tenant-room-list'),
     path('tenant/rooms/', TenantRoomListView.as_view(), name='tenant-room-list'),
    # path('tenant/<uuid:tenant_id>/room/<int:room_id>/', TenantRoomDetailView.as_view(), name='tenant-room-detail'),
    path('tenant/room/<int:room_id>/', TenantRoomDetailView.as_view(), name='tenant-room-detail'),
    path('agent/report-inventory/<uuid:id>/',AgentInventoryView.as_view(),name="agent-report-inventory")
]


	# 69948f52-60fb-4f7e-a534-8fafe222d33f
   