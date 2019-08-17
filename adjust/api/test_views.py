from django.test import TestCase, Client
import os, django

from api.models import PerformanceMetric
from api.views import metrics

os.environ['DJANGO_SETTINGS_MODULE'] =  "api.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()

# set up the client
client = Client()

class RestApiTest(TestCase):
    def setUp(self):
        client.get("/load/")
        print("initial data setup done")

    def test_default_api_status_code(self):
        response  = client.get("/metrics/")
        self.assertEqual(response.status_code,200)
    
    def test_api_1(self):
        response  = client.get("/metrics/?group=channel,country&agg=impressions,clicks&where={\"date_to\":\"2017-06-01\"}&sort=-clicks")
        json_data = response.json()
        self.assertTrue(len(json_data['data']) > 0)
    
    def test_api_2(self):
        response  = client.get("/metrics/?where={\"date_from\":\"2017-05-01\",\"date_to\":\"2017-05-31\"}&group=date&agg=installs&sort=date")
        json_data = response.json()
        self.assertTrue(len(json_data['data']) > 0)
    
    def test_api_3(self):
        response  = client.get("/metrics/?where={\"country\":\"US\",\"date\":\"2017-06-01\"}&group=os&agg=revenue&sort=-revenue")
        json_data = response.json()
        self.assertTrue(len(json_data['data']) > 0)

    def test_api_4(self):
        response  = client.get("/metrics/?where={\"country\":\"CA\"}&group=channel&agg=-cpi,-spend&sort=-cpi")
        json_data = response.json()
        self.assertTrue(len(json_data['data']) > 0)