import django_filters
from ..models import Award


class AwardFilter(django_filters.FilterSet):
    player = django_filters.UUIDFilter(field_name="player__id")
    status = django_filters.CharFilter()
    season = django_filters.CharFilter()
    competition = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Award
        fields = ["player", "status", "season", "competition"]
