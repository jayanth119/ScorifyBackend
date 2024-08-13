from django.contrib import admin
from .models import MouldHumidity 
class MouldHumidityAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'avg_humidity_30_days', 'ventilation_score')
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(MouldHumidity, MouldHumidityAdmin)