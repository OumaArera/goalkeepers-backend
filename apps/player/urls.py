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
]
