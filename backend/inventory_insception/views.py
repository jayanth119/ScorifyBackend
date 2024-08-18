# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . models import Room,Inspection
from . serializers import RoomSerializer,InspectionSerializer

# from ..core.models import Inspection
# from .InventorySeriliazer import InspectionSerializer


# @api_view(['GET', 'POST'])
# def inspection_list(request):
#     if request.method == 'GET':
#         inspections = Inspection.objects.all()
#         serializer = InspectionSerializer(inspections, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'POST':
#         serializer = InspectionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT'])
# def inspection_detail(request, inspection_id):
#     try:
#         inspection = Inspection.objects.get(id=inspection_id)
#     except Inspection.DoesNotExist:
#         return Response({"error": "Inspection not found"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = InspectionSerializer(inspection)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'PUT':
#         serializer = InspectionSerializer(inspection, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomList(APIView):
    def get(self,request):
        room=Room.objects.all()
        serializer=RoomSerializer(rooms,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class RoomDetails(APIView):
    def get(self,request,room_id):
        try:
            room=Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=RoomSerializer(room)

        return Response(serializer.data,status=status.HTTP_200_OK)

class InspectionList(APIView):        
    def get(self,request):
        inspections=Inspection.objects.all()
        serializer=InspectionSerializer(inspections,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class InspectionDetails(APIView):
    def get(self,request,inspection_id):
        try:
            inspection=Inspection.objects.get(id=inspection_id)

        except Inspection.DoesNotExist:

            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=InspectionSerializer(inspection)

        return Response(serializer.data,status=status.HTTP_200_OK)
        

