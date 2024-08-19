from rest_framework.serializers import ModelSerializer
from . models import Room,Condition,Defect,Inventory


class ConditionSerializer(ModelSerializer):
    class Meta:
        model=Condition
        fields=['id','item','condition','cleanliness','photo']

class DefectSerializer(ModelSerializer):
    class Meta:
        model=Defect
        fields=['id','description']

class RoomSerializer(ModelSerializer):                                                                                          
    conditions=ConditionSerializer(many=True,read_only=True)
    defects=DefectSerializer(many=True,read_only=True)
    class Meta:
        model=Room
        fields=['id','name','completion_percentage','conditions','defects']

class InventorySerializer(ModelSerializer):
    rooms=RoomSerializer(many=True,read_only=True)
    
    class Meta:
        model=Inventory
        fields=['id','property','document','score','date','type','title','created_by','expiry_date','past_inventory','rooms']



