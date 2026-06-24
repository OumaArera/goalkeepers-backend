# from rest_framework import serializers
# from ..models import *


# class GoalkeeperAwardEventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GoalkeeperAwardEvent
#         fields = "__all__"


# class GoalkeeperAwardCategorySerializer(serializers.ModelSerializer):
#     event_title = serializers.CharField(
#         source="event.title",
#         read_only=True
#     )

#     class Meta:
#         model = GoalkeeperAwardCategory
#         fields = "__all__"


# class GoalkeeperAwardNominationSerializer(serializers.ModelSerializer):
#     player_name = serializers.CharField(
#         source="player.get_full_name",
#         read_only=True
#     )

#     category_name = serializers.CharField(
#         source="category.name",
#         read_only=True
#     )

#     class Meta:
#         model = GoalkeeperAwardNomination
#         fields = "__all__"


# class GoalkeeperAwardWinnerSerializer(serializers.ModelSerializer):
#     player = serializers.CharField(
#         source="nomination.player.get_full_name",
#         read_only=True
#     )

#     category = serializers.CharField(
#         source="nomination.category.name",
#         read_only=True
#     )

#     event = serializers.CharField(
#         source="nomination.category.event.title",
#         read_only=True
#     )

#     class Meta:
#         model = GoalkeeperAwardWinner
#         fields = "__all__"
