from django.contrib import admin
from .models import BloodRequest, DonorResponse, BedRequest

class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'blood_group', 'location_city', 'status', 'created_at')
    list_filter = ('status', 'blood_group', 'urgency')

class DonorResponseAdmin(admin.ModelAdmin):
    list_display = ('donor', 'blood_request', 'status', 'created_at')
    list_filter = ('status',)

class BedRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'hospital', 'bed_type', 'priority', 'status', 'created_at')
    list_filter = ('status', 'bed_type', 'priority')

admin.site.register(BloodRequest, BloodRequestAdmin)
admin.site.register(DonorResponse, DonorResponseAdmin)
admin.site.register(BedRequest, BedRequestAdmin)
