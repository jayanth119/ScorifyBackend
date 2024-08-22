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
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)  # Expose user_id as the primary key
    properties = PropertyIDSerializer(many=True, read_only=True)
    tenants = TenantIDSerializer(many=True, read_only=True)

    class Meta:
        model = Landlord
        fields = ['user_id', 'name', 'phone', 'email', 'properties', 'tenants']  # Use 'user_id' instead of 'id'

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
class TenantPropertyDashboardSerializer(serializers.ModelSerializer):
    # You would include methods to calculate or retrieve the required data such as scores, counts, etc.
    class Meta:
        model = Property
        fields = ['address', 'zip_code', 'property_type', 'house_age', 'epc_status', 'risk_assessment_percentage', 
                  'mould_ventilation_percentage', 'next_inspection_date', 'inspection_count', 'inventory_count', 
                  'open_repair_count', 'regular_maintenance', 'tenant', 'agent']  # Add other necessary fields

        def get_tenant_info(self, obj):
            return {
                "name": obj.tenant.name,
                "phone_number": obj.tenant.phone
            }

        def get_agent_info(self, obj):
            return {
                "name": obj.agent.name,
                "phone_number": obj.agent.phone
            }

        tenant = serializers.SerializerMethodField()
        agent = serializers.SerializerMethodField()

class LandlordPropertyDashboardSerializer(serializers.ModelSerializer):
    tenant_details = serializers.SerializerMethodField()
    inspection_details = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['address', 'zip_code', 'property_type', 'house_age', 'epc_status', 
                  'next_inspection_date', 'inspection_count', 'open_repair_count', 'tenant_details', 
                  'inspection_details']

    def get_tenant_details(self, obj):
        tenants = obj.tenants.all()
        return [
            {"name": tenant.name, "phone_number": tenant.phone, "email": tenant.email} for tenant in tenants
        ]

    def get_inspection_details(self, obj):
        inspections = obj.inspections.all()
        return [
            {"date": inspection.date, "type": inspection.type, "score": inspection.score} for inspection in inspections
        ]
