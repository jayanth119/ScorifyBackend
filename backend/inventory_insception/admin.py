from django.contrib import admin
from .models import Room, Condition, Inventory, Defect,AgentLandlord
from core.models import Tenant

class InventoryAdmin(admin.ModelAdmin):
    list_display=('id','property','score','date','type','title','created_by','expiry_date','past_inventory')
    readonly_fields=('id',)

class RoomAdmin(admin.ModelAdmin):
    list_display=('id','name','completion_percentage','inventory')
    search_fields=('name','inventory__id','inventory__property__name')
    list_filter=('inventory',)  

class ConditionAdmin(admin.ModelAdmin):
    list_display=('id','room','item','condition','cleanliness')
    search_fields=('room__name','item')
    list_filter=('condition','room')

class DefectAdmin(admin.ModelAdmin):
    list_display=('id','room','description')
    search_fields=('room__name','description')

class AgentLandlordAdmin(admin.ModelAdmin):
    list_display=('agent','landlord')
    search_fields=('agent__name','landlord__name')

class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'landlord', 'is_verified']
    list_filter=('is_verified',) 
    # search_fields = ['name', 'email', 'phone']



admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Defect, DefectAdmin)
admin.site.register(AgentLandlord,AgentLandlordAdmin)
# admin.site.register(Tenant,TenantAdmin)
