import django_filters
from ..models.player import Player


class PlayerFilter(django_filters.FilterSet):
    min_height = django_filters.NumberFilter(field_name="height", lookup_expr="gte")
    max_height = django_filters.NumberFilter(field_name="height", lookup_expr="lte")
    country = django_filters.CharFilter(method="filter_country")

    class Meta:
        model = Player
        fields = [
            "country_of_birth",
            "country_of_residence",
            "is_active",
            "sex",
            "injured",
            "first_name",
            "last_name",
            "preferred_foot",
        ]

    def filter_country(self, queryset, name, value):
        return queryset.filter(
            country_of_birth__icontains=value
        ) | queryset.filter(
            country_of_residence__icontains=value
        )
