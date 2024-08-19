from rest_framework.serializers import ModelSerializer
from .models import Maintenance,Repair
from core.models import Property
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

class PropertySerializer(ModelSerializer):
    class Meta:
        model = Property
        fields = ['address','open_repair_count','house_age']
class AgentRepairSerializer(ModelSerializer):
    property = PropertySerializer()
    class Meta:
        model = Repair
        fields = ['id','property','description','status']

class RepairSerializer(ModelSerializer):
    class Meta:
        model = Repair
        fields = "__all__"

class TenantOpenRepairSerializer(ModelSerializer):
    class Meta:
        model = Repair
        fields = ['id','repair_score','description','status','completion_date']
class TenantRepairHistorySerializer(ModelSerializer):
    class Meta:
        model = Repair
        fields = ['id','description','status','completion_date','completion_report']