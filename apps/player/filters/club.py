import django_filters
from ..models import Club


class ClubFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(lookup_expr="iexact")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Club
        fields = ["country", "is_active"]
