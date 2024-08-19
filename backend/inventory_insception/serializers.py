from rest_framework import serializers
from . model import Room,Condition,Defect,Inspection

class ConditionSerializer(serializer.ModalSerializer):
    class Meta:
        model=Condition
        fields=['id','item','condition','cleanliness','photo','document']

class DefectSerializer(serializer.ModalSerializer):
    class Meta:
        model=Defect
        fields=['id','description']

class RoomSerializer(serializer.ModalSerializer):
    conditions=ConditionSerializer(many=True,read_only=True)
    defects=DefectSerializer(many=True,read_only=True)
    class Meta:
        model=Room
        field=['id','name','completion_percentage','conditions','defects']

class InspectionSerializer(serializer.ModalSerializer):
    rooms=RoomSerializer(many=True,read_only=True)
    
    class Meta:
        model=Inspection
        field=['id','property','document','score','date','type','title','created_by','expiry_date','past_inspection','rooms']

