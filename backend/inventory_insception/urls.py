from django.urls import path
from . views import RoomList,RoomDetails,InventoryList,InventoryDetails,InventoryRooms,InventoryRoomDetails

urlpatterns = [
    path('rooms/',RoomList.as_view(),name='room-list'),   #Thiis 
    path('rooms/<uuid:room_id>/',RoomDetails.as_view(),name='room-detail'),   #This is the just for testing for getting rooms
    path('landlords/inventory/', InventoryList.as_view(), name='inventory-list'),  
    path('landlords/inventory/<uuid:inventory_id>/', InventoryDetails.as_view(), name='inventory-detail'),
    path('landlords/inventory/<uuid:inven_id>/rooms/',InventoryRooms.as_view(),name='inventory-rooms'),
    path('landlords/inventory/<uuid:inven_id>/rooms/<uuid:room_id>/',InventoryRoomDetails.as_view(),name='inventory-room-details'),    
]
