from django.contrib import admin
from .models import GasSafety , HeatingSafety 
# Register your models here.

class HeatingSafetyAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'boiler_condition', 'controller', 'radiators_condition')
    readonly_fields = ('id',)


@admin.register(GasSafety)
class GasSafetyAdmin(admin.ModelAdmin):
    list_display = ('property', 'repair_score', 'report_date', 'due_date', 'current_eer', 'potential_eer')
    search_fields = ('property__address', 'repair_score', 'current_eer', 'potential_eer')
    list_filter = ('current_eer', 'potential_eer', 'due_date')
    readonly_fields = ('id',)

admin.site.register(HeatingSafety, HeatingSafetyAdmin)