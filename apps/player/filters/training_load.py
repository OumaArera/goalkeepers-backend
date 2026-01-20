import django_filters
from ..models import TrainingLoad


class TrainingLoadFilter(django_filters.FilterSet):
    player = django_filters.UUIDFilter(field_name="player__id")
    session_type = django_filters.CharFilter()
    date_from = django_filters.DateFilter(
        field_name="session_date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="session_date", lookup_expr="lte"
    )

    class Meta:
        model = TrainingLoad
        fields = [
            "player",
            "session_type",
            "status",
        ]
