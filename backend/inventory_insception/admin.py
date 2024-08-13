from django.contrib import admin
from .models import Room , Condition ,Inspection 


class InspectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'score', 'date', 'type')
    readonly_fields = ('id',)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'completion_percentage', 'inspection')
    search_fields = ('name', 'inspection__id', 'inspection__name')
    list_filter = ('inspection',)

class ConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'item', 'condition')
    search_fields = ('room__name', 'item')
    list_filter = ('condition', 'room')
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Condition, ConditionAdmin)