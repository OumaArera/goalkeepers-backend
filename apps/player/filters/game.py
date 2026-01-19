import django_filters
from ..models import Game


class GameFilter(django_filters.FilterSet):
    match_date = django_filters.DateFromToRangeFilter()
    competition = django_filters.CharFilter(lookup_expr="icontains")
    season = django_filters.CharFilter(lookup_expr="iexact")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Game
        fields = [
            "match_date",
            "competition",
            "season",
            "is_active",
        ]
