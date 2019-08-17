from django.test import TestCase

from api.models import PerformanceMetric

# Create your tests here.
class PerformanceMetricTest(TestCase):
    """Simple testcase for performance model"""
    def setUp(self):
        PerformanceMetric.objects.create(
            date = '2019-08-17',
            channel='unit-test',
            country='DE',
            os='mac',
            clicks = 10,
            installs=5,
            spend = 100,
            impressions = 10,
            revenue = 20
        )

    def test_prop_values(self):
        sample_object = PerformanceMetric.objects.get(id=1)
        self.assertEqual(sample_object.channel,"unit-test")
        self.assertEqual(sample_object.country,"DE")