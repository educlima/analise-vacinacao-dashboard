from rest_framework import serializers
from .models import VaccineData

class VaccineDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineData
        fields = ["id", "country", "state_or_region", "date", "vaccinated", "deaths", "population"]
