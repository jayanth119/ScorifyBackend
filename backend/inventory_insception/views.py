# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . models import Room,Inventory
from core.models import Tenant,Landlord
from . serializers import RoomSerializer,InventorySerializer,LandLordInventorySerializer,LandLordDetailSerializer,TenantWithLandlordSerializer


class RoomList(APIView):
    def get(self,request):
        room=Room.objects.all()
        serializer=RoomSerializer(room,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class RoomDetails(APIView):
    def get(self,request,room_id):
        try:
            room=Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=RoomSerializer(room,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class InventoryList(APIView):        
    def get(self,request):
        inventory=Inventory.objects.all()
        serializer=InventorySerializer(inventory,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class InventoryDetails(APIView):
    def get(self,request,inventory_id):
        try:
            inventory=Inventory.objects.get(id=inventory_id)

        except Inventory.DoesNotExist:

            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=InventorySerializer(inventory)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class InventoryRooms(APIView):
    def get(self,request,inventory_id):
        inventory=Inventory.objects.get(id=inventory_id)
        rooms=Room.objects.filter(inventory=inventory)
        serializer=RoomSerializer(rooms,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class InventoryRoomDetails(APIView):
    def get(self,request,inventory_id,room_id):
        inventory=Inventory.objects.get(id=inventory_id)
        room=Room.objects.get(inventory=inventory)
        serializer=RoomSerializer(room)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class AgentLandlordInventoryListView(APIView):
    def get(self,request,agent_id):
        inventories=Inventory.objects.filter(landlord__landlord_agents__agent_id=agent_id)
        serializer=LandLordInventorySerializer(inventories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AgentSpecificLandlordInventoryDetailView(APIView):
    def get(self,request,agent_id,landlord_id):
        inventories=Inventory.objects.filter(landlord__landlord_agents__agent_id=agent_id,landlord_id=landlord_id)
        serializer=LandLordDetailSerializer(inventories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)




class TenantInventoryView(APIView):
    def get(self,request,tenant_id):
        try:
            tenant=Tenant.objects.get(id=tenant_id)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=TenantWithLandlordSerializer(tenant)
        return Response(serializer.data,status=status.HTTP_200_OK)


    

        
    

        

