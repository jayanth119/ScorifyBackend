from rest_framework.serializers import ModelSerializer
from . models import Room,Condition,Inventory,AgentLandlord
from core.models import Landlord,Property,Tenant



#Landlord Serializers

class ConditionSerializer(ModelSerializer):
    class Meta:
        model=Condition
        fields=['id','item']


class RoomSerializer(ModelSerializer):                                                                                          
    conditions=ConditionSerializer(many=True,read_only=True)
    class Meta:
        model=Room
        fields=['id','name','completion_percentage','conditions']

class InventorySerializer(ModelSerializer):
    rooms=RoomSerializer(many=True,read_only=True)
    
    class Meta:
        model=Inventory
        fields=['id','property','document','score','date','type','title','created_by','expiry_date','past_inventory','rooms']

#Agent serializers

class LandLordInventorySerializer(ModelSerializer):
    class Meta:
        model=Inventory
        fields=['property_address','document','condition','created_by','date']


class LandLordDetailSerializer(ModelSerializer):
    class Meta:
        model=Inventory
        fields=['property_address','document','condition','created_by','date']

class AgentLandlordSerializer(ModelSerializer):
    class Meta:
        model=AgentLandlord
        fields=['agent', 'landlord']


#Tenant serializer


class PropertySerializer(ModelSerializer):
    class Meta:
        model=Property
        fields=['id','name','address','description']

class LandlordSerializer(ModelSerializer):
    properties=PropertySerializer(many=True,read_only=True)
    inventory=InventorySerializer(many=True,read_only=True)
    class Meta:
        model=Landlord
        fields=['id','name','phone','email','inventory','properties']

class TenantWithLandlordSerializer(ModelSerializer):
    landlord=LandlordSerializer(read_only=True)
    class Meta:
        model=Tenant
        fields=['name','phone','email','occupation','landlord']
    
