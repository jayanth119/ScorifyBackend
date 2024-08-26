# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework.response import Response
from . models import Room,Inventory , Condition , Inspection 
from core.models import Tenant,Landlord,Agent,Property
from . serializers import RoomSerializer,InventorySerializer,LandLordInventorySerializer,LandLordDetailSerializer,TenantWithLandlordSerializer,AgentInventorySerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
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
    def get(self, request, inventory_id, room_id):
        # Retrieve the inventory object or return 404 if not found
        inventory = get_object_or_404(Inventory, id=inventory_id)
        
        # Retrieve the room object or return 404 if not found
        room = get_object_or_404(Room, inventory=inventory, id=room_id)
        
        # Serialize the room object
        serializer = RoomSerializer(room)
        
        # Return the serialized data with HTTP 200 status
        return Response(serializer.data, status=status.HTTP_200_OK)

    

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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            tenant = Tenant.objects.get(user=request.user)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TenantWithLandlordSerializer(tenant)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TenantRoomListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            tenant = Tenant.objects.get(user=request.user)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

        rooms = Room.objects.filter(inventory__property__in=tenant.properties.all())
        room_list = []

        for room in rooms:
            total_items = Condition.objects.filter(room=room).count()
            completed_inspections = Inspection.objects.filter(room=room, is_completed=True).count()
            next_inspection = Inspection.objects.filter(room=room, is_completed=False).order_by('due_date').first()
            next_inspection_date = next_inspection.due_date if next_inspection else None

            room_list.append({
                "room_id": room.id,
                "name": room.name,
                "total_items": total_items,
                "completed_inspections": completed_inspections,
            })

        return Response({
            "next_inspection_date": next_inspection_date,
            "rooms": room_list
        }, status=status.HTTP_200_OK)


class TenantRoomDetailView(APIView):
    def get(self, request, room_id):
        try:
            tenant = Tenant.objects.get(user=request.user)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

        room = get_object_or_404(Room, id=room_id, inventory__property__in=tenant.properties.all())
        conditions = Condition.objects.filter(room=room)
        total_items = conditions.count()
        completed_inspections = Inspection.objects.filter(room=room, is_completed=True).count()

        condition_list = []
        for condition in conditions:
            condition_list.append({
                "condition_id": condition.id,
                "condition": condition.item  # Assuming you meant to refer to the 'item' field here
            })

        return Response({
            "room_id": room.id,
            "name": room.name,
            "completion_percentage": room.completion_percentage,
            "total_items": total_items,
            "completed_inspections": completed_inspections,
            "conditions": condition_list
        }, status=status.HTTP_200_OK)


class AgentInventoryView(APIView):
    def get(self, request, id):
        try:
            agent = Agent.objects.get(user__id=id)
            landlords = agent.landlords.all()
            data = []
            
            for landlord in landlords:
                inventories = Inventory.objects.filter(property__in=landlord.properties.all())
                serializer = AgentInventorySerializer(inventories, many=True)
                
                data.append({
                    # 'landlord': landlord.id, 
                    'inventories': serializer.data
                })
            
            return Response(data, status=status.HTTP_200_OK)
        except Agent.DoesNotExist:
            return Response({"error": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)

