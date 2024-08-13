from django.contrib import admin

from epc.models import EPCReport

# Register your models here.
class EPCReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'score', 'report_date', 'current_score', 'potential_score')
    readonly_fields = ('id',)
admin.site.register(EPCReport, EPCReportAdmin)