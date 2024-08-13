from django.contrib import admin
from . models import Maintenance , Repair 
# Register your models here.
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'status', 'completion_date')
    readonly_fields = ('id',)

class RepairAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'status', 'completion_date', 'cost')
    readonly_fields = ('id',)



admin.register(Maintenance , MaintenanceAdmin )
admin.site.register(Repair, RepairAdmin)