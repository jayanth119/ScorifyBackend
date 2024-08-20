from django.contrib import admin
from .models import Room, Condition, Inventory, Defect

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'score', 'date', 'type', 'title', 'created_by', 'expiry_date', 'past_inventory')
    readonly_fields = ('id',)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'completion_percentage', 'get_inspection')  # Changed from 'inspection' to 'get_inspection'
    search_fields = ('name',)
    list_filter = ('completion_percentage',)  # Removed 'inspection' from list_filter

    def get_inspection(self, obj):
        # Assuming that Room has a ForeignKey to Inspection, modify this according to your actual models
        return obj.inspection.id if obj.inspection else "No Inspection"
    get_inspection.short_description = 'Inspection'

class ConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'item', 'condition', 'cleanliness')
    search_fields = ('room__name', 'item')
    list_filter = ('condition', 'room')

class DefectAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'description')
    search_fields = ('room__name', 'description')

admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Defect, DefectAdmin)
