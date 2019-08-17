import os
from .models import PerformanceMetric
from .services import QueryBuilder
from django.http import JsonResponse


# Need to repare this method
def load_inital_data(request):
    return_resposne = {
        "message" : "Loaded successfully"
    }
    if not os.path.exists("dataset.csv"):
        return_resposne["message"] = "Unable to find dataset.csv file"
    else:
        import csv;
        with open("dataset.csv")  as dataset:
            dataset_csv_reader = csv.DictReader(dataset,delimiter=',')
            for row in dataset_csv_reader:
                metric = PerformanceMetric(
                    date = row['date'],
                    channel = row['channel'],
                    country = row['country'],
                    os = row['os'],
                    impressions = row['impressions'],
                    clicks = row['clicks'],
                    installs = row['installs'],
                    spend = row['spend'],
                    revenue = row['revenue']
                )
                metric.save()
    return JsonResponse(return_resposne)

# Common API
def metrics(request):
    query_builder = QueryBuilder(PerformanceMetric,request)
    data = query_builder.build()
    return JsonResponse({"data":data})
    