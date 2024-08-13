from django.contrib import admin
from .models import SafetyAssessment , RiskAssessment 
# Register your models here.

class SafetyAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'score', 'electricity_condition', 'gas_condition')
    readonly_fields = ('id',)

class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'title', 'date', 'expiry_date')
    readonly_fields = ('id',)


admin.site.register(SafetyAssessment, SafetyAssessmentAdmin)
admin.site.register(RiskAssessment, RiskAssessmentAdmin)