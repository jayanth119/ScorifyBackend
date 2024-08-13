from django.contrib import admin
from .models import GasSafety , HeatingSafety 
# Register your models here.
class GasSafetyAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'report_date', 'title', 'current_eer', 'potential_eer')
    readonly_fields = ('id',)

class HeatingSafetyAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'boiler_condition', 'controller', 'radiators_condition')
    readonly_fields = ('id',)


admin.site.register(GasSafety, GasSafetyAdmin)
admin.site.register(HeatingSafety, HeatingSafetyAdmin)