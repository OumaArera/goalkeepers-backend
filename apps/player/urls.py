from django.urls import path
from .views import *

urlpatterns = [
    path(
        "players/",
        PlayerListCreateAPIView.as_view(), 
        name="player-list-create"
    ),
    path(
        "players/<uuid:id>/", 
        PlayerRetrieveUpdateAPIView.as_view(), 
        name="player-detail"
    ),
    path(
        "games/", 
        GameListCreateAPIView.as_view(), 
        name="game-list-create"
    ),
    path(
        "games/<uuid:id>/", 
        GameRetrieveUpdateAPIView.as_view(), 
        name="game-detail"
    ),
    path(
        "goalkeeper-stats/",
        GoalkeeperStatsListCreateAPIView.as_view(),
        name="goalkeeper-stats-list-create"
    ),
    path(
        "goalkeeper-stats/<uuid:id>/",
        GoalkeeperStatsRetrieveUpdateAPIView.as_view(),
        name="goalkeeper-stats-detail"
    ),
    path(
        "goalkeeper-stats/<uuid:id>/approve/",
        GoalkeeperStatsApprovalAPIView.as_view(),
        name="goalkeeper-stats-approve"
    ),

    path("clubs/", ClubListCreateAPIView.as_view(), name="club-list-create"),
    path("clubs/<uuid:id>/", ClubRetrieveUpdateAPIView.as_view(), name="club-detail"),

    path("awards/", AwardListCreateAPIView.as_view(), name="award-list-create"),
    path("awards/<uuid:id>/", AwardRetrieveUpdateAPIView.as_view(), name="award-detail"),
    path("awards/<uuid:id>/approve/", AwardApprovalAPIView.as_view(), name="award-approve"),

    path("physical-health/", HealthAssessmentListCreateAPIView.as_view()),
    path("physical-health/<uuid:id>/", HealthAssessmentRetrieveUpdateAPIView.as_view()),
    path("physical-health/<uuid:id>/approve/", HealthAssessmentApprovalAPIView.as_view()),
]
