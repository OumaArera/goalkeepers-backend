import django_filters
from ..models import PhysicalHealthAssessment


class PhysicalHealthAssessmentFilter(django_filters.FilterSet):
    player = django_filters.UUIDFilter(field_name="player__id")
    game = django_filters.UUIDFilter(field_name="game__id")
    assessment_type = django_filters.CharFilter()
    date_from = django_filters.DateFilter(
        field_name="assessment_date", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="assessment_date", lookup_expr="lte"
    )

    class Meta:
        model = PhysicalHealthAssessment
        fields = [
            "player",
            "game",
            "assessment_type",
            "status",
        ]
