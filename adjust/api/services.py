from django.db.models import Sum,Avg,Count,F,ExpressionWrapper,FloatField
from django.db.models.query import QuerySet
import json
from .models import PerformanceMetric
from django.core import serializers

EMPTY_LIST = []
EMPTY_DICT = {}
class QueryBuilder:
    """
        Name  : QueryBuilder
        Input : Model and request
        Desc  : Generic takes model and applies filter,group and aggregation 
                return json response upon calling build method
    """
    def __init__(self,model,request):
        "Default intitailizer to initaialize the default values of the variables"
        self.agg = request.GET.get('agg',[])
        self.group = request.GET.get('group',[])
        self.where = request.GET.get('where',{})
        self.sort = request.GET.get('sort',[])
        self.model = model
        self.qs = QuerySet(model)
        self.agg_literal_map = {
            '+' : Sum,
            '-' : Avg,
            '*' : Count
        }
        self.agg_map = {}

    def _get_agg_col_mapping(self,column):
        """
            Input : column
            Ouput: 
                If the first char starts any one of the below then below mappings
                are applied or by default Sum is applied
                    + -> Sum
                    - -> Avg
                    * -> Count
            e.g,:
                +col1 -> Avg(col1)
        """
        _aggregation = Sum
        _column = column

        if (column[0] in self.agg_literal_map):
            _aggregation = self.agg_literal_map[column[0]]
            _column = column[1:]

        self.agg_map[_column] = _aggregation(_column)

    def _get_agg(self):
        """
            Splits the agg param from the request and _get_agg_col_mapping 
            is invoked to construct aggregation map
        """
        if self.agg is not None:
            columns = self.agg.split(",")
            for column in columns:
                self._get_agg_col_mapping(column)

        return self.agg_map

    def _get_group(self):
        """
            Splits the group param from the request otherwise returns empty list
        """
        if len(self.group):
            return [field for field in self.group.split(",")]
        return EMPTY_LIST
    
    def _get_where(self):
        """
            Converts the JSON type string where clause to dict
            Custmisation done only for date_to and date_from which are mapped 
            to out of the box date__gte and date__lte fields
        """
        if self.where:
            json_where_clause = json.loads(self.where)
            if 'date_from' in json_where_clause:
                json_where_clause["date__gte"] = json_where_clause["date_from"]
                del json_where_clause["date_from"]
            if 'date_to' in json_where_clause:
                json_where_clause["date__lte"] = json_where_clause["date_to"]
                del json_where_clause["date_to"]
            return json_where_clause
        return EMPTY_DICT

    def _get_order_by(self):
        """
            If Sort param is present then splits otherwise return emptylist
        """
        if self.sort:
            return self.sort.split(",")
        return EMPTY_LIST

    def build(self):
        """
         From queryset applies filter,group,sort and agg methods accordingly
        """
        is_group_by = False

        # caluclated field CPI
        cpi = ExpressionWrapper(F('spend')/F('installs'),output_field=FloatField())
        self.qs = self.qs.annotate(cpi=cpi)

        # Aggreation are applied here
        if len(self._get_group()) > 0 and len(self._get_agg()) > 0:
            is_group_by = True
            self.qs = self.qs.values(*self._get_group()) \
                             .annotate(**self._get_agg())

         # Where clause if applied here
        if len(self._get_where()) > 0:
            self.qs = self.qs.filter(**self._get_where())

        # Sorting is applied
        if len(self._get_order_by()) > 0:
            self.qs = self.qs.order_by(*self._get_order_by())
        
        # return the list of PeformanceMetric user
        if is_group_by:
            return list(self.qs)
        else:
            self.qs = self.qs.values()
            return list(self.qs)

       