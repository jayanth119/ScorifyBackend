
from .serializers import MaintenanceServiceSerializer,MaintenanceScheduleSerailizer,AgentRepairSerializer,LandlordRepairSerializer,AgentMaintenanceSerializer,TenantRepairHistorySerializer,TenantMaintenanceScheduleSerializer
from rest_framework.views import APIView
from .models import Maintenance,Repair
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from django.contrib.auth import get_user_model

Customuser = get_user_model()
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
    parser_classes = [MultiPartParser,FormParser]
    def get(self,request,tenant_id):
       maintenance = Maintenance.objects.filter(performed_by='tenant')
       serializer = MaintenanceScheduleSerailizer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,tenant_id):
       
       request.data['user']=tenant_id
       serializer = TenantMaintenanceScheduleSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data,status=status.HTTP_200_OK)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

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