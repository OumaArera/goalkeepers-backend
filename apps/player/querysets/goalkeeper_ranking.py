from django.db.models import (
    Avg, Count, Sum, FloatField, IntegerField, ExpressionWrapper, Q, F
)
from django.db.models.functions import Cast, Coalesce, NullIf
from apps.player.models import Player
from ..models import GoalkeeperStat


def goalkeeper_ranking_queryset(year=None):
    stats = GoalkeeperStat.objects.filter(
        status=GoalkeeperStat.Status.APPROVED
    )

    if year:
        stats = stats.filter(game__match_date__year=year)

    return (
        Player.objects
        .filter(goalkeeper_stats__in=stats)
        .distinct()
        .annotate(
            matches_played=Count(
                "goalkeeper_stats",
                filter=Q(goalkeeper_stats__in=stats),
                distinct=True
            ),
            avg_saves=Coalesce(
                Avg("goalkeeper_stats__saves", filter=Q(goalkeeper_stats__in=stats)),
                0.0
            ),
            avg_goals_conceded=Coalesce(
                Avg("goalkeeper_stats__goals_conceded", filter=Q(goalkeeper_stats__in=stats)),
                0.0
            ),
            errors_per_game=Coalesce(
                Avg(
                    Cast("goalkeeper_stats__error_leading_to_goal", FloatField()),
                    filter=Q(goalkeeper_stats__in=stats)
                ),
                0.0
            ),
            clean_sheets=Coalesce(
                Sum(
                    Cast("goalkeeper_stats__clean_sheet", IntegerField()),
                    filter=Q(goalkeeper_stats__in=stats)
                ),
                0
            ),
        )
        .annotate(
            clean_sheet_rate=ExpressionWrapper(
                Cast("clean_sheets", FloatField()) /
                Cast("matches_played", FloatField()),
                output_field=FloatField()
            )
        )
        .annotate(
            ranking_score=ExpressionWrapper(
                (F("avg_saves") * 1.5)
                + (F("clean_sheets") * 3)
                - (F("goals_conceded") * 1.2),
                output_field=FloatField(),
            )
        )
    )
