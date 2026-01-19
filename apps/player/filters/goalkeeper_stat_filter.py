import django_filters
from ..models import GoalkeeperStat


class GoalkeeperStatFilter(django_filters.FilterSet):
    game = django_filters.UUIDFilter()
    player = django_filters.UUIDFilter()
    status = django_filters.CharFilter()

    class Meta:
        model = GoalkeeperStat
        fields = ["game", "player", "status"]
