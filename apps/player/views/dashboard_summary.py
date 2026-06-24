from datetime import date
from django.utils.timezone import now
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from calendar import monthrange
from django.db import models
from apps.player.models import *
from ...user.models import User
from ...common import ApiResponse


class DashboardSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        start_of_month = today.replace(day=1)

        # ─────────────────────────────
        # Players
        # ─────────────────────────────
        player_totals = Player.objects.aggregate(
            total=Count("id"),
            male=Count("id", filter=models.Q(sex=Player.Sex.MALE)),
            female=Count("id", filter=models.Q(sex=Player.Sex.FEMALE)),
            unverified=Count("id", filter=models.Q(user__is_verified=False)),
        )

        # ─────────────────────────────
        # Clubs
        # ─────────────────────────────
        club_totals = Club.objects.aggregate(
            total=Count("id"),
            unverified=Count("id", filter=models.Q(is_active=False)),
        )

        # ─────────────────────────────
        # Games
        # ─────────────────────────────
        end_of_month = today.replace(
            day=monthrange(today.year, today.month)[1]
        )

        game_totals = Game.objects.aggregate(
            upcoming_total=Count(
                "id",
                filter=models.Q(match_date__gte=today)
            ),
            upcoming_this_month=Count(
                "id",
                filter=models.Q(
                    match_date__gte=today,
                    match_date__lte=end_of_month
                )
            ),
        )

        # ─────────────────────────────
        # Goalkeeper Stats
        # ─────────────────────────────
        stat_totals = GoalkeeperStat.objects.aggregate(
            total=Count("id"),
            pending=Count(
                "id",
                filter=models.Q(status=GoalkeeperStat.Status.PENDING)
            ),
        )

        # ─────────────────────────────
        # Physical Health Assessments
        # ─────────────────────────────
        health_totals = PhysicalHealthAssessment.objects.aggregate(
            total=Count("id"),
            pending=Count(
                "id",
                filter=models.Q(status=PhysicalHealthAssessment.Status.PENDING)
            ),
        )

        # ─────────────────────────────
        # Training Load
        # ─────────────────────────────
        training_totals = TrainingLoad.objects.aggregate(
            total=Count("id"),
            pending=Count(
                "id",
                filter=models.Q(status=TrainingLoad.Status.PENDING)
            ),
        )

        # ─────────────────────────────
        # Users (per role)
        # ─────────────────────────────
        users_queryset = User.objects.exclude(role="bold")

        users_total = users_queryset.count()
        users_by_role = (
            users_queryset
            .values("role")
            .annotate(total=Count("id"))
            .order_by()
        )

        return ApiResponse.success(
            data={
                "players": player_totals,
                "clubs": club_totals,
                "games": game_totals,
                "goalkeeper_stats": stat_totals,
                "physical_health": health_totals,
                "training_load": training_totals,
                "users": {
                    "total": users_total,
                    "by_role": list(users_by_role),
                },
            }
        )
