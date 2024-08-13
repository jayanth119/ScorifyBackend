from rest_framework import generics
from core.models import Landlord, Tenant, Agent , Property 
from core.LATserializer  import LandlordSerializer, TenantSerializer, AgentSerializer,PropertySerializer

# View to retrieve details of a Landlord by ID
class LandlordDetailView(generics.RetrieveAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    lookup_field = 'id'  # Use UUID field to look up the landlord

# View to retrieve details of a Tenant by ID
class TenantDetailView(generics.RetrieveAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    lookup_field = 'id'  # Use UUID field to look up the tenant

# View to retrieve details of an Agent by ID
class AgentDetailView(generics.RetrieveAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    lookup_field = 'id'  # Use UUID field to look up the agent

# View to list all Landlords
class LandlordListView(generics.ListAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer

# View to list all Tenants
class TenantListView(generics.ListAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

# View to list all Agents
class AgentListView(generics.ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'id'  # Use UUID field to look up the property

# View to list all Properties
class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer