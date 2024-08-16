from django.shortcuts import render
from .serializers import MaintenanceServiceSerializer,MaintenanceScheduleSerailizer,MaintenanceUpcomingSerializer
from rest_framework.views import APIView
from .models import Maintenance
from rest_framework.response import Response
from rest_framework import status
class PerformedByMixin(APIView):
    performed_by = None
    
    def get(self, request):
        if not self.performed_by:
            return Response({"error": "No performed_by value specified"}, status=status.HTTP_400_BAD_REQUEST)
        
        maintenance = Maintenance.objects.filter(performed_by=self.performed_by)
        serializer = MaintenanceServiceSerializer(maintenance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LandlordScheduleList(APIView):
    def get(self,request):
       maintenance = Maintenance.objects.filter(performed_by='landlord')
       serializer = MaintenanceScheduleSerailizer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)
class AgentScheduleList(APIView):
    def get(self,request):
       maintenance = Maintenance.objects.filter(performed_by='agent')
       serializer = MaintenanceScheduleSerailizer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)
class TenantScheduleList(APIView):
    def get(self,request):
       maintenance = Maintenance.objects.filter(performed_by='tenant')
       serializer = MaintenanceScheduleSerailizer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)
    
class LandlordUpcomingList(APIView):
    def get(self,request):
       maintenance = Maintenance.objects.filter(performed_by='landlord')
       serializer = MaintenanceUpcomingSerializer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)
