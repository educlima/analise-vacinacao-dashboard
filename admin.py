from django.contrib import admin
from .models import VaccineData

@admin.register(VaccineData)
class VaccineDataAdmin(admin.ModelAdmin):
    list_display = ["country", "state_or_region", "date", "vaccinated", "deaths"]
    list_filter = ["country", "date"]
    search_fields = ["state_or_region"]
