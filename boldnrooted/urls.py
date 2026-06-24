from django.urls import path 
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

urlpatterns = [
    # Authentication endpoints
    path('blogs/', BlogListCreateAPIView.as_view(), name='blogs-create'),
    path('blogs/', BlogRetrieveUpdateAPIView.as_view(), name='blogs-retrive'),
    path(
        'retrieve-blogs/<uuid:id>/',
        BlogRetrieveUpdateAPIView.as_view(),
        name='blogs-retrieve'
    ),
    path('scriptures/', ScriptureReferenceListCreateAPIView.as_view(), name='scripture-create'),
    path('scriptures/<uuid:id>/', ScriptureReferenceRetrieveUpdateAPIView.as_view(), name='scriptures-retrive'),
    path('tags/', TagListCreateAPIView.as_view(), name='scripture-tags'),
    path('tags/<uuid:id>/', TagRetrieveUpdateAPIView.as_view(), name='scriptures-tags'),
    path('programs/', ProgramListCreateAPIView.as_view(), name='programs-tags'),
    path('programs/<uuid:id>/', ProgramRetrieveUpdateAPIView.as_view(), name='programs-tags'),

    path(
        "discipleship/",
        DiscipleshipTrackListCreateAPIView.as_view(),
        name="discipleship-list"
    ),

    path(
        "discipleship/<uuid:id>/",
        DiscipleshipTrackRetrieveUpdateAPIView.as_view(),
        name="discipleship-detail"
    ),
    path(
        "discipleship-modules/",
        DiscipleshipModuleListCreateAPIView.as_view(),
        name="discipleship-module-list"
    ),

    path(
        "discipleship-modules/<uuid:id>/",
        DiscipleshipModuleRetrieveUpdateAPIView.as_view(),
        name="discipleship-module-detail"
    ),
    path(
        "events/",
        EventListCreateAPIView.as_view(),
        name="events-create"
    ),

    path(
        "events/<uuid:id>/",
        EventRetrieveUpdateAPIView.as_view(),
        name="events-retrieve"
    ),
    path(
        "prayer-categories/",
        PrayerCategoryListCreateAPIView.as_view(),
        name="prayer-categories"
    ),

    path(
        "prayer-categories/<uuid:id>/",
        PrayerCategoryRetrieveUpdateAPIView.as_view(),
        name="prayer-category-detail"
    ),

    path(
        "prayer-requests/",
        PrayerRequestListCreateAPIView.as_view(),
        name="prayer-requests"
    ),

    path(
        "prayer-requests/<uuid:id>/",
        PrayerRequestRetrieveUpdateAPIView.as_view(),
        name="prayer-request-detail"
    ),

    path(
        "prayer-requests/<uuid:id>/pray/",
        PrayForRequestAPIView.as_view(),
        name="pray-for-request"
    ),
    path(
        "join-us/",
        JoinRequestListCreateAPIView.as_view(),
        name="join-us"
    ),

    path(
        "join-us/<uuid:id>/",
        JoinRequestRetrieveUpdateAPIView.as_view(),
        name="join-us-detail"
    ),
]