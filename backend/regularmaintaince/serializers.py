from rest_framework.serializers import ModelSerializer
from .models import Maintenance,Repair
from core.LATserializer import PropertySerializer
class MaintenanceServiceSerializer(ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id','score','completion_date','details','status','report_photos','performed_by','report']


class MaintenanceScheduleSerailizer(ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id','score','title','description','status','due_date','report_photos']

class MaintenanceUpcomingSerializer(ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id','score','due_date','upcoming_photo']

class AgentRepairSerializer(ModelSerializer):
    property = PropertySerializer()
    class Meta:
        model = Repair
        fields = ['id','property','description','status']
class AgentMaintenanceSerializer(ModelSerializer):
    property = PropertySerializer()
    class Meta:
        model = Repair
        fields = ['id','property']

class LandlordRepairSerializer(ModelSerializer):
    class Meta:
        model = Repair 
        fields = ['user_id','completion_date','cost','description','status','repair_score']

class TenantRepairHistorySerializer(ModelSerializer):
    class Meta:
        model = Repair 
        fields = ['id','description','status','completion_date']