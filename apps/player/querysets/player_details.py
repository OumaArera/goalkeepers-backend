from django.db.models import (
    Avg, Sum, Count, OuterRef, Subquery,
    FloatField, IntegerField, ExpressionWrapper
)
from django.core.cache import cache
from django.db.models.functions import Coalesce, Cast
from ..constants import (
    GOALKEEPER_STAT_AVG_FIELDS,
    PHYSICAL_HEALTH_AVG_FIELDS,
    TRAINING_LOAD_SUM_FIELDS,
    TRAINING_LOAD_AVG_FIELDS,
)
from ..models import *

def player_base_queryset():
    return (
        Player.objects
        .select_related("user")
        .prefetch_related(
            "appearances",
            "play_styles",
            "club_memberships__club",
            "awards",
        )
    )


def player_list_queryset():
    base = player_base_queryset()

    base_gk_stats = GoalkeeperStat.objects.filter(
        player=OuterRef("pk"),
        status=GoalkeeperStat.Status.APPROVED
    )

    annotations = {}

    for field in GOALKEEPER_STAT_AVG_FIELDS:
        annotations[f"avg_{field}"] = Coalesce(
            Subquery(
                base_gk_stats
                .values("player")
                .annotate(v=Avg(field))
                .values("v")[:1],
                output_field=FloatField()
            ),
            0.0
        )

    annotations["clean_sheet_rate"] = Coalesce(
        Subquery(
            base_gk_stats
            .values("player")
            .annotate(
                rate=ExpressionWrapper(
                    Cast(
                        Sum(Cast("clean_sheet", IntegerField())),
                        FloatField()
                    ) /
                    Cast(Count("id"), FloatField()),
                    output_field=FloatField()
                )
            )
            .values("rate")[:1]
        ),
        0.0
    )

    return base.annotate(**annotations)


def player_detail_analytics(player, year=None):
    cache_key = f"player:{player.id}:analytics:{year or 'all'}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    # ─────────────────────────────
    # Goalkeeper Stats (last 20 games)
    # ─────────────────────────────
    gk_stats = player.goalkeeper_stats.filter(
        status=GoalkeeperStat.Status.APPROVED
    )

    if year:
        gk_stats = gk_stats.filter(game__match_date__year=year)

    gk_last_20 = gk_stats.select_related("game").order_by("-game__match_date")[:20]

    gk_recent = list(
        gk_last_20.values(
            "id",
            "game_id",
            "game__match_date",
            *GOALKEEPER_STAT_AVG_FIELDS,
            "clean_sheet",
        )
    )


    gk_aggregates = gk_stats.aggregate(
        **{field: Avg(field) for field in GOALKEEPER_STAT_AVG_FIELDS},
        clean_sheet_rate=Cast(
            Sum(Cast("clean_sheet", IntegerField())),
            FloatField()
        ) / Cast(Count("id"), FloatField()),
        matches_played=Count("id"),
    )

    gk_averages = {
        field: gk_aggregates.get(field) or 0
        for field in GOALKEEPER_STAT_AVG_FIELDS
    }


    gk_clean_sheet_rate = (
        gk_stats.aggregate(
            rate=Cast(Sum(Cast("clean_sheet", IntegerField())), FloatField()) /
                 Cast(Count("id"), FloatField())
        )["rate"] or 0
    )

    # ─────────────────────────────
    # Physical Health (last 20)
    # ─────────────────────────────
    health_qs = player.health_assessments.filter(
        status=PhysicalHealthAssessment.Status.APPROVED
    )

    if year:
        health_qs = health_qs.filter(assessment_date__year=year)

    health_last_20 = health_qs.order_by("-assessment_date")[:20]

    health_aggregates = health_qs.aggregate(
        **{field: Avg(field) for field in PHYSICAL_HEALTH_AVG_FIELDS},
        records=Count("id"),
    )

    health_averages = {
        field: health_aggregates.get(field) or 0
        for field in PHYSICAL_HEALTH_AVG_FIELDS
    }


    # ─────────────────────────────
    # Training Load (last 20)
    # ─────────────────────────────
    training_qs = player.training_loads.filter(
        status=TrainingLoad.Status.APPROVED
    )

    if year:
        training_qs = training_qs.filter(session_date__year=year)

    training_last_20 = training_qs.order_by("-session_date")[:20]

    training_aggregates = training_qs.aggregate(
        **{field: Sum(field) for field in TRAINING_LOAD_SUM_FIELDS},
        **{field: Avg(field) for field in TRAINING_LOAD_AVG_FIELDS},
        sessions=Count("id"),
    )

    training_sums = {
        field: training_aggregates.get(field) or 0
        for field in TRAINING_LOAD_SUM_FIELDS
    }

    training_averages = {
        field: training_aggregates.get(field) or 0
        for field in TRAINING_LOAD_AVG_FIELDS
    }


    # ─────────────────────────────
    # Final Response Structure
    # ─────────────────────────────
    data = {
        "goalkeeper": {
            "recent": gk_recent,
            "averages": gk_averages,
            "clean_sheet_rate": gk_clean_sheet_rate,
            "matches_played": gk_aggregates.get("matches_played") or 0,
        },
        "physical_health": {
            "recent": list(health_last_20.values()),
            "averages": health_averages,
            "records": health_aggregates.get("records") or 0,
        },
        "training_load": {
            "recent": list(training_last_20.values()),
            "totals": training_sums,
            "averages": training_averages,
            "sessions": training_aggregates.get("sessions") or 0,
        },
    }

    cache.set(cache_key, data, timeout=60 * 5)
    return data

    # cache.set(cache_key, data, timeout=60 * 5)
    # return {
    #     "goalkeeper": {
    #         "recent": list(
    #             gk_last_20.values(
    #                 "id",
    #                 "game_id",
    #                 "match_date",
    #                 *GOALKEEPER_STAT_AVG_FIELDS,
    #                 "clean_sheet"
    #             )
    #         ),
    #         "averages": gk_averages,
    #         "clean_sheet_rate": round(gk_clean_sheet_rate, 3),
    #         "matches_played": gk_stats.count(),
    #     },
    #     "physical_health": {
    #         "recent": list(health_last_20.values()),
    #         "averages": health_averages,
    #         "records": health_qs.count(),
    #     },
    #     "training_load": {
    #         "recent": list(training_last_20.values()),
    #         "totals": training_sums,
    #         "averages": training_averages,
    #         "sessions": training_qs.count(),
    #     },
    # }
