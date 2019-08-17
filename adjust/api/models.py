from django.db import models

# Create your models here.
class PerformanceMetric(models.Model):
    """
        Model to store performance metrice information
    """
    date = models.DateField()
    channel = models.CharField(max_length=100)
    country = models.CharField(max_length=5) # Assuming ISO country code format and will not need
    os = models.CharField(max_length=50) # Assuming os can change value other than android and ios
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    installs = models.IntegerField()
    spend = models.DecimalField(max_digits=20,decimal_places=2)
    revenue = models.DecimalField(max_digits=20,decimal_places=2)

    @staticmethod
    def fields():
        return [ f.name for f in PerformanceMetric._meta.fields ]