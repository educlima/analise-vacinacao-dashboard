from django.db import models

class VaccineData(models.Model):
    country = models.CharField(max_length=100)
    state_or_region = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    vaccinated = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    population = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ["country", "state_or_region", "date"]
        ordering = ["-date"]
        indexes = [
            models.Index(fields=['country']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.country} - {self.state_or_region} - {self.date}"
