from django.urls import path
from . views import RoomList,RoomDetails,InspectionList,InspectionDetails

urlpatterns = [
    path('rooms/',RoomList.as_view(),name='room-list'),
    path('rooms/<uuid:room_id>/',RoomDetails.as_view(),name='room-detail')
    path('inventory/', InspectionList.as_view(), name='inspection-list'),
    path('inventory/<uuid:inspection_id>/', InspectionDetails.as_view(), name='inspection-detail'),
]
#