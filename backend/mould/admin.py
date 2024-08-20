from django.contrib import admin
from .models import MouldHumidity,VentilationItem
class MouldHumidityAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'avg_humidity_30_days', 'ventilation_score')
    readonly_fields = ('id',)

admin.site.register(VentilationItem)
# Register your models here.
admin.site.register(MouldHumidity, MouldHumidityAdmin)
# admin.site.register(Ventilation, VentilationAdmin)