from django.shortcuts import render
from .serializers import MaintenanceServiceSerializer,MaintenanceScheduleSerailizer,AgentRepairSerializer,LandlordRepairSerializer,AgentMaintenanceSerializer,TenantRepairHistorySerializer
from rest_framework.views import APIView
from .models import Maintenance,Repair
from rest_framework.response import Response
from rest_framework import status

class LandlordMaintenanceServiceHistory(APIView):
    def get(self,request,user_id):
       maintenance = Maintenance.objects.filter(user__id=user_id)
       serializer = MaintenanceServiceSerializer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)

class AgentMaintenanceView(APIView):
    def get(self,request,user_id):
       repair= Repair.objects.filter(user__id=user_id)
       serializer = AgentMaintenanceSerializer(repair,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)
    

class LandlordScheduleList(APIView):
    def get(self,request,user_id):
       maintenance = Maintenance.objects.filter(user__id=user_id)
       serializer = MaintenanceScheduleSerailizer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)

class TenantScheduleList(APIView):
    def get(self,request):
       maintenance = Maintenance.objects.filter(performed_by='tenant')
       serializer = MaintenanceScheduleSerailizer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)

# class LandlordUpcomingList(APIView):
#     def get(self,request):
#        maintenance = Maintenance.objects.filter(performed_by='landlord')
#        serializer = MaintenanceUpcomingSerializer(maintenance,many=True)
#        return Response(serializer.data,status=status.HTTP_200_OK)
    
class AgentOpenRepairView(APIView):
    def get(self,request,user_id):
        repair = Repair.objects.filter(user__id=user_id)
        serializer = AgentRepairSerializer(repair,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class LandlordRepairHistoryView(APIView):
    def get(self,request,user_id):
        repairs = Repair.objects.filter(user__id=user_id)
        if repairs.exists():
            serializer = LandlordRepairSerializer(repairs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No repairs found for this user."}, status=status.HTTP_404_NOT_FOUND)

class TenantRepairHistoryView(APIView):
    def get(self,request,user_id):
        repairs = Repair.objects.filter(user__id=user_id)
        if repairs.exists():
            serializer = TenantRepairHistorySerializer(repairs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No repairs found for this user."}, status=status.HTTP_404_NOT_FOUND)