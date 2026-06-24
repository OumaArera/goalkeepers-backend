import django_filters
from ..models import Program


class ProgramFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="start_date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="end_date", lookup_expr="lte")
    title = django_filters.CharFilter(lookup_expr="icontains")
    organizer = django_filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = Program
        fields = ["title", "organizer", "start_date", "end_date"]