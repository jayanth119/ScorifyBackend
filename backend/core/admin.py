from django.contrib import admin
from .models import (
    Landlord, Property, Tenant, Agent,
    PropertyTimeline, HousePhoto, SalesManagement, Management, LettingManagement
)

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')
    filter_horizontal = ('properties',)
    readonly_fields = ('user',)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'landlord')
    search_fields = ('name', 'phone', 'email', 'landlord__name')
    filter_horizontal = ('properties',)
    readonly_fields = ('user',)

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'location', 'website')
    search_fields = ('name', 'phone', 'email', 'location')
    filter_horizontal = ('landlords', 'tenants')
    readonly_fields = ('user',)

# @admin.register(Landlord)
# class LandlordAdmin(admin.ModelAdmin):
#     list_display = ('name', 'phone', 'email')
#     search_fields = ('name', 'phone', 'email')
#     filter_horizontal = ('properties',)  # Only include many-to-many fields
#     readonly_fields = ('id',)

# @admin.register(Tenant)
# class TenantAdmin(admin.ModelAdmin):
#     list_display = ('name', 'phone', 'email', 'landlord')
#     search_fields = ('name', 'phone', 'email', 'landlord__name')
#     filter_horizontal = ('properties',)  # Only include many-to-many fields
#     readonly_fields = ('id',)

# @admin.register(Agent)
# class AgentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'phone', 'email', 'location', 'website')
#     search_fields = ('name', 'phone', 'email', 'location')
#     filter_horizontal = ('landlords', 'tenants')  # These should be many-to-many fields
#     readonly_fields = ('id',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'house_name', 'zip_code')
    readonly_fields = ('id',)

@admin.register(PropertyTimeline)
class PropertyTimelineAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'date', 'maintenance_repair_type')
    readonly_fields = ('id',)

@admin.register(HousePhoto)
class HousePhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'name', 'photo_type', 'uploaded_date')
    readonly_fields = ('id',)

@admin.register(SalesManagement)
class SalesManagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'landlord_property', 'details')
    search_fields = ('agent__name', 'landlord_property__address', 'details')
    list_filter = ('agent',)

@admin.register(LettingManagement)
class LettingManagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'tenant_property', 'landlord_property', 'details')
    search_fields = ('agent__name', 'tenant_property__address', 'landlord_property__address', 'details')
    list_filter = ('agent',)

@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'property')
    readonly_fields = ('id',)
