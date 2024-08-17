from .views import PerformedByMixin
class LandlordServiceList(PerformedByMixin):
    performed_by = 'landlord'

class AgentServiceList(PerformedByMixin):
    performed_by = 'agent'

class TenantServiceList(PerformedByMixin):
    performed_by = 'tenant'

 # Assuming this should also filter by landlord
