from django.contrib import admin
from .models import Room, Condition, Inspection, Defect

class InspectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'score', 'date', 'type', 'title', 'created_by', 'expiry_date', 'past_inspection')
    readonly_fields = ('id',)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'completion_percentage', 'inspection')
    search_fields = ('name', 'inspection__id', 'inspection__property__name')
    list_filter = ('inspection',)

class ConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'item', 'condition', 'cleanliness')
    search_fields = ('room__name', 'item')
    list_filter = ('condition', 'room')

class DefectAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'description')
    search_fields = ('room__name', 'description')

admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Defect, DefectAdmin)
