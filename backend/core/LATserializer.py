from rest_framework import serializers
from core.models import Landlord, Tenant, Agent, Property

class PropertyIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id']  # Only include the ID field

class TenantIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id']  # Only include the ID field

class TenantSerializer(serializers.ModelSerializer):
    landlord = serializers.PrimaryKeyRelatedField(read_only=True)  # Only the ID of the landlord
    properties = PropertyIDSerializer(many=True, read_only=True)  # Only the IDs of properties

    class Meta:
        model = Tenant
        fields = ['id', 'name', 'phone', 'email', 'current_tenancy_score', 'landlord', 'properties']

class LandlordSerializer(serializers.ModelSerializer):
    properties = PropertyIDSerializer(many=True, read_only=True)  # Only the IDs of properties
    tenants = TenantIDSerializer(many=True, read_only=True)  # Only the IDs of tenants

    class Meta:
        model = Landlord
        fields = ['id', 'name', 'phone', 'email', 'properties', 'tenants']

class AgentSerializer(serializers.ModelSerializer):
    landlords = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Only the IDs of landlords
    tenants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Only the IDs of tenants

    class Meta:
        model = Agent
        fields = ['id', 'name', 'phone', 'email', 'location', 'website', 'landlords', 'tenants']


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'address', 'house_name', 'zip_code', 'bathroom_count', 'living_room_count', 'property_type', 'house_age', 'floor_map_photos', 'epc_status', 'risk_assessment_percentage', 'mould_ventilation_percentage', 'gas_safety', 'heat_safety', 'start_date', 'end_date', 'deposit', 'details', 'next_inspection_date', 'open_repair_count', 'inspection_count', 'regular_maintenance', 'inventory_count']
