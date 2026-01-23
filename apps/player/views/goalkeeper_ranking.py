from django.db.models import (
    Count, Sum, Avg, F, FloatField, ExpressionWrapper, Q
)
from rest_framework import generics
from rest_framework.permissions import AllowAny

from ..models import Player
from ..serializers.goalkeeper_ranking import GoalkeeperRankingSerializer
from ...common import ApiResponse, StandardPagination
from ..models import GoalkeeperStat


class GoalkeeperRankingAPIView(generics.ListAPIView):
    serializer_class = GoalkeeperRankingSerializer
    pagination_class = StandardPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        approved = GoalkeeperStat.Status.APPROVED

        return (
            Player.objects
            .filter(goalkeeper_stats__status=approved)
            .annotate(
                matches_played=Count(
                    "goalkeeper_stats",
                    filter=Q(goalkeeper_stats__status=approved),
                    distinct=True,
                ),

                avg_saves=Avg(
                    "goalkeeper_stats__saves",
                    filter=Q(goalkeeper_stats__status=approved),
                ),

                clean_sheets=Count(
                    "goalkeeper_stats",
                    filter=Q(
                        goalkeeper_stats__status=approved,
                        goalkeeper_stats__clean_sheet=True,
                    ),
                ),

                goals_conceded=Sum(
                    "goalkeeper_stats__goals_conceded",
                    filter=Q(goalkeeper_stats__status=approved),
                ),
            )
            .annotate(
                ranking_score=ExpressionWrapper(
                    (F("avg_saves") * 1.5)
                    + (F("clean_sheets") * 3)
                    - (F("goals_conceded") * 1.2),
                    output_field=FloatField(),
                )
            )
            .order_by("-ranking_score")
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ApiResponse.success(
            data=response.data,
            meta={"count": self.paginator.page.paginator.count},
        )
