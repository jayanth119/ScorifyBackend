from rest_framework import serializers
from .models import Maintenance,Repair,MaintenanceImage
from core.LATserializer import PropertySerializer
class MaintenanceServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id','score','completion_date','details','status','report_photos','performed_by','report']


class MaintenanceScheduleSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id','score','title','description','status','due_date','report_photos']

class MaintenanceUpcomingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id','score','due_date','upcoming_photo']

class AgentRepairSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    class Meta:
        model = Repair
        fields = ['id','property','description','status']
class AgentMaintenanceSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    class Meta:
        model = Repair
        fields = ['id','property']

class LandlordRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair 
        fields = ['user_id','completion_date','cost','description','status','repair_score']

class TenantRepairHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair 
        fields = ['id','description','status','completion_date']

class MaintenanceScheduleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceImage
        fields = "__all__"
class TenantMaintenanceScheduleSerializer(serializers.ModelSerializer):
    images = MaintenanceScheduleImageSerializer(many=True,read_only=True)
    uploaded_images = uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = Maintenance
        fields =['id','uploaded_images','user','images']

    def create(self, validated_data):
        images_data = validated_data.pop('uploaded_images')
        maintenance = Maintenance.objects.create(**validated_data)
        for image in images_data:
            MaintenanceImage.objects.create(maintenance=maintenance)