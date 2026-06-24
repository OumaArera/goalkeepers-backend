# import django_filters as filters
# from ..models import *

# class GoalkeeperAwardEventFilter(filters.FilterSet):
#     status = filters.CharFilter(field_name="status")
#     year = filters.NumberFilter(field_name="event_date", lookup_expr="year")

#     class Meta:
#         model = GoalkeeperAwardEvent
#         fields = ["status"]


# class GoalkeeperAwardNominationFilter(filters.FilterSet):
#     category = filters.UUIDFilter(field_name="category_id")
#     player = filters.UUIDFilter(field_name="player_id")
#     status = filters.CharFilter(field_name="status")

#     class Meta:
#         model = GoalkeeperAwardNomination
#         fields = ["category", "player", "status"]
