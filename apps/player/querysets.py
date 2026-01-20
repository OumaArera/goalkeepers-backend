from django.db.models import (
    Avg, Sum, Count, OuterRef, Subquery,
    FloatField, IntegerField, ExpressionWrapper
)
from django.db.models.functions import Coalesce, Cast
from .constants import (
    GOALKEEPER_STAT_AVG_FIELDS,
    PHYSICAL_HEALTH_AVG_FIELDS,
    TRAINING_LOAD_SUM_FIELDS,
    TRAINING_LOAD_AVG_FIELDS,
)
from .models import *


def player_list_queryset():
    base_gk_stats = GoalkeeperStat.objects.filter(
        player=OuterRef("pk"),
        status=GoalkeeperStat.Status.APPROVED
    )

    annotations = {}

    # ─── AVG for all numeric columns (NO booleans) ───────────
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

    # ─── Clean sheet rate (Postgres-safe) ────────────────────
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

    return (
        Player.objects
        .select_related("user")
        .annotate(**annotations)
        .prefetch_related(
            "club_memberships__club",
            "awards",
        )
    )


def player_detail_analytics(player, year=None):
    # ─────────────────────────────
    # Goalkeeper Stats (last 20 games)
    # ─────────────────────────────
    gk_stats = player.goalkeeper_stats.filter(
        status=GoalkeeperStat.Status.APPROVED
    )

    if year:
        gk_stats = gk_stats.filter(game__match_date__year=year)

    gk_last_20 = gk_stats.select_related("game").order_by("-game__match_date")[:20]

    gk_averages = {
        field: gk_stats.aggregate(v=Avg(field))["v"] or 0
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

    health_averages = {
        field: health_qs.aggregate(v=Avg(field))["v"] or 0
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

    training_sums = {
        field: training_qs.aggregate(v=Sum(field))["v"] or 0
        for field in TRAINING_LOAD_SUM_FIELDS
    }

    training_averages = {
        field: training_qs.aggregate(v=Avg(field))["v"] or 0
        for field in TRAINING_LOAD_AVG_FIELDS
    }

    # ─────────────────────────────
    # Final Response Structure
    # ─────────────────────────────
    return {
        "goalkeeper": {
            "recent": list(gk_last_20.values()),
            "averages": gk_averages,
            "clean_sheet_rate": round(gk_clean_sheet_rate, 3),
            "matches_played": gk_stats.count(),
        },
        "physical_health": {
            "recent": list(health_last_20.values()),
            "averages": health_averages,
            "records": health_qs.count(),
        },
        "training_load": {
            "recent": list(training_last_20.values()),
            "totals": training_sums,
            "averages": training_averages,
            "sessions": training_qs.count(),
        },
    }
